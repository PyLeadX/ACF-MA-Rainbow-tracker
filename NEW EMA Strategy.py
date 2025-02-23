// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Lorienzo_C

//@version=5
strategy("EMA Crossover Strategy with Manual Reversal Patterns", overlay=true)

// Input parameters
ema10_length = input(10, title="EMA 10 Length")
ema21_length = input(21, title="EMA 21 Length")
ema50_length = input(50, title="EMA 50 Length")
ema200_length = input(200, title="EMA 200 Length")

// Calculate EMAs
ema10 = ta.ema(close, ema10_length)
ema21 = ta.ema(close, ema21_length)
ema50 = ta.ema(close, ema50_length)
ema200 = ta.ema(close, ema200_length)

// Entry conditions
buy_condition = ta.crossover(ema10, ema21) and ema10 > ema21 and ema21 > ema50 and ema50 > ema200
sell_condition = ta.crossunder(ema10, ema21) and ema10 < ema21 and ema21 < ema50 and ema50 < ema200

// ✅ Fixed Reversal Pattern Conditions
bullish_engulfing = close[1] < open[1] and close > open and close > open[1] and open < close[1]
bearish_engulfing = close[1] > open[1] and close < open and close < close[1] and open > open[1]
bullish_harami = close[1] < open[1] and close > open and close < open[1] and open > close[1]
bearish_harami = close[1] > open[1] and close < open and close > open[1] and open < close[1]
hammer = close > open and (high - low) > 3 * (close - open) and (close - low) / (high - low) > 0.6
inverted_hammer = close > open and (high - low) > 3 * (close - open) and (high - close) / (high - low) > 0.6

// ✅ Fixed Exit Conditions with 3% Tolerance for EMA50
tolerance = 0.03 * close  // 3% price tolerance

if (bullish_engulfing or bullish_harami or inverted_hammer)
    if (math.abs(close - ema50) < tolerance)  
        strategy.close("Buy")

if (bearish_engulfing or bearish_harami or hammer)
    if (math.abs(close - ema50) < tolerance)  
        strategy.close("Sell")

// Strategy entry logic
if (buy_condition)
    strategy.entry("Buy", strategy.long)

if (sell_condition)
    strategy.entry("Sell", strategy.short)

// Plot EMAs
plot(ema10, color=color.red, title="EMA 10")
plot(ema21, color=color.green, title="EMA 21")
plot(ema50, color=color.blue, title="EMA 50")
plot(ema200, color=color.yellow, title="EMA 200")
