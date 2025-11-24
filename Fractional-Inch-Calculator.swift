//
// FractionalInchCalculator.swift
// Single-file SwiftUI iOS app implementing a fractional-inch calculator.
// Paste into a new Swift file in Xcode (or replace ContentView in a new SwiftUI App).
//

import SwiftUI
import Foundation

@main
struct FractionalInchCalculatorApp: App {
    var body: some Scene {
        WindowGroup {
            FractionalInchCalculatorView()
        }
    }
}

struct FractionalInchCalculatorView: View {
    @State private var inputA: String = "1 3/8"
    @State private var inputB: String = "2.25"
    @State private var operationIndex = 0 // 0 = add, 1 = subtract
    @State private var selectedDenominatorIndex = 5
    @State private var resultDecimal: Double? = nil
    @State private var resultFractionText: String = ""
    @State private var errorMessage: String? = nil

    let operations = ["+", "−"]
    let denominators = [2, 4, 8, 16, 32, 64]

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Inputs")) {
                    VStack(alignment: .leading) {
                        Text("Value A (e.g. 1 3/8, 3/16, 2.25)")
                            .font(.caption)
                        TextField("Value A", text: $inputA)
                            .keyboardType(.numbersAndPunctuation)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                    }

                    HStack {
                        Picker("", selection: $operationIndex) {
                            ForEach(0..<operations.count) { idx in
                                Text(operations[idx]).tag(idx)
                            }
                        }
                        .pickerStyle(SegmentedPickerStyle())
                        .frame(width: 90)
                        VStack(alignment: .leading) {
                            Text("Value B")
                                .font(.caption)
                            TextField("Value B", text: $inputB)
                                .keyboardType(.numbersAndPunctuation)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                        }
                    }
                }

                Section(header: Text("Precision")) {
                    Picker("Fraction Denominator", selection: $selectedDenominatorIndex) {
                        ForEach(0..<denominators.count) { idx in
                            Text("1/\(denominators[idx])").tag(idx)
                        }
                    }
                    .pickerStyle(SegmentedPickerStyle())
                }

                Section {
                    HStack {
                        Spacer()
                        Button("Calculate") {
                            calculate()
                        }
                        .buttonStyle(.borderedProminent)
                        Spacer()
                    }
                }

                Section(header: Text("Result")) {
                    if let err = errorMessage {
                        Text(err).foregroundColor(.red)
                    } else if let dec = resultDecimal {
                        Text("Decimal inches: \(formatDecimal(dec))")
                        Text("Fraction: \(resultFractionText)")
                    } else {
                        Text("No result yet. Tap Calculate.")
                    }
                }
            }
            .navigationTitle("Fractional Inch Calc")
        }
    }

    func calculate() {
        errorMessage = nil
        resultDecimal = nil
        resultFractionText = ""

        guard let a = parseFractionString(inputA) else {
            errorMessage = "Could not parse Value A."
            return
        }
        guard let b = parseFractionString(inputB) else {
            errorMessage = "Could not parse Value B."
            return
        }

        let raw: Double
        if operationIndex == 0 {
            raw = a + b
        } else {
            raw = a - b
        }

        resultDecimal = raw
        let denom = denominators[selectedDenominatorIndex]
        resultFractionText = formatAsFraction(raw, maxDenominator: denom)
    }

    // MARK: - Parsing and formatting

    // Accepts "1 3/8", "1-3/8", "3/16", "2.25", ".5", "-1 1/2" etc.
    func parseFractionString(_ s: String) -> Double? {
        let str = s.trimmingCharacters(in: .whitespacesAndNewlines)
        if str.isEmpty { return nil }

        // Try plain Double first
        if let d = Double(str.replacingOccurrences(of: ",", with: "")) {
            return d
        }

        // Replace hyphens with space to handle "1-3/8"
        let normalized = str.replacingOccurrences(of: "-", with: " ").replacingOccurrences(of: "—", with: " ")

        // Detect negative sign
        var working = normalized
        var sign: Double = 1.0
        if working.hasPrefix("-") {
            sign = -1.0
            working = String(working.dropFirst()).trimmingCharacters(in: .whitespaces)
        } else if working.hasPrefix("+") {
            working = String(working.dropFirst()).trimmingCharacters(in: .whitespaces)
        }

        let parts = working.split(separator: " ").map { String($0) }
        if parts.count == 2, parts[1].contains("/") {
            // mixed number "1 3/8"
            if let whole = Double(parts[0]), let frac = parseSimpleFraction(parts[1]) {
                return sign * (whole + frac)
            }
        } else if parts.count == 1, parts[0].contains("/") {
            // simple fraction "3/16"
            if let frac = parseSimpleFraction(parts[0]) {
                return sign * frac
            }
        } else {
            // fallback: try to parse components like " 3 / 16 "
            let joined = working.replacingOccurrences(of: " ", with: "")
            if joined.contains("/") {
                if let frac = parseSimpleFraction(joined) {
                    return sign * frac
                }
            }
        }

        return nil
    }

    // parse "3/8" or " 3/ 8 "
    func parseSimpleFraction(_ s: String) -> Double? {
        let cleaned = s.replacingOccurrences(of: " ", with: "")
        let parts = cleaned.split(separator: "/").map { String($0) }
        guard parts.count == 2, let num = Double(parts[0]), let den = Double(parts[1]), den != 0 else {
            return nil
        }
        return num / den
    }

    func formatAsFraction(_ value: Double, maxDenominator: Int) -> String {
        if value.isInfinite || value.isNaN {
            return "Invalid"
        }
        if value == 0 {
            return "0"
        }

        let sign = value < 0 ? "-" : ""
        let absValue = abs(value)
        let whole = Int(floor(absValue))
        let fractional = absValue - Double(whole)

        // Find best numerator for given maxDenominator using rounding
        let rawNumerator = Int((fractional * Double(maxDenominator)).rounded())
        var numerator = rawNumerator
        var denominator = maxDenominator

        // Simplify fraction
        if numerator == 0 {
            if whole == 0 {
                return "\(sign)0"
            } else {
                return "\(sign)\(whole)\""
            }
        }

        // If numerator equals denominator, bump whole up
        if numerator == denominator {
            return "\(sign)\(whole + 1)\""
        }

        let g = gcd(numerator, denominator)
        numerator /= g
        denominator /= g

        if whole == 0 {
            return "\(sign)\(numerator)/\(denominator)\""
        } else {
            return "\(sign)\(whole) \(numerator)/\(denominator)\""
        }
    }

    func formatDecimal(_ value: Double) -> String {
        // Show up to 6 decimal places and trim trailing zeros
        let formatter = NumberFormatter()
        formatter.minimumFractionDigits = 0
        formatter.maximumFractionDigits = 6
        formatter.numberStyle = .decimal
        return formatter.string(from: NSNumber(value: value)) ?? "\(value)"
    }

    func gcd(_ a0: Int, _ b0: Int) -> Int {
        var a = abs(a0)
        var b = abs(b0)
        if b == 0 { return a }
        while b != 0 {
            let t = a % b
            a = b
            b = t
        }
        return a
    }
}