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


// Reversal pattern identification
bullish_engulfing = close[1] < open[1] and close > open and close < low[1] and open < low[1]
bearish_engulfing = close[1] > open[1] and close < open and close > high[1] and open > high[1]
bullish_harami = close[1] > open[1] and close < open and close > low[1] and open < low[1]
bearish_harami = close[1] < open[1] and close > open and close < high[1] and open > high[1]
hammer = close > open and (high - low) > 3 * (open - close) and (close - low) / (0.001 + high - low) > 0.6
inverted_hammer = close > open and (high - low) > 3 * (open - close) and (high - close) / (0.001 + high - low) > 0.6


// Strategy entry and exit
if (buy_condition)
    strategy.entry("Buy", strategy.long)


if (sell_condition)
    strategy.entry("Sell", strategy.short)


if (bullish_engulfing or bullish_harami or inverted_hammer)
    if (close == ema50)
        strategy.close("Buy")


if (bearish_engulfing or bearish_harami or hammer)
    if (close == ema50)
        strategy.close("Sell")


// Plot EMAs
plot(ema10, color=color.red, title="EMA 10")
plot(ema21, color=color.green, title="EMA 21")
plot(ema50, color=color.blue, title="EMA 50")
plot(ema200, color=color.yellow, title="EMA 200")


#ADD1 AND USE Additional EMA Crossovers


ema5_length = input(5, title="EMA 5 Length")
ema5 = ta.ema(close, ema5_length)

short_term_buy = ta.crossover(ema5, ema10)
short_term_sell = ta.crossunder(ema5, ema10)

if (short_term_buy)
    strategy.entry("Short-Term Buy", strategy.long)

if (short_term_sell)
    strategy.entry("Short-Term Sell", strategy.short)



#ADD2 AND Overbought/Oversold Conditions


rsi_length = input(14, title="RSI Length")
rsi = ta.rsi(close, rsi_length)

buy_rsi_condition = rsi < 30
sell_rsi_condition = rsi > 70

if (buy_rsi_condition)
    strategy.entry("RSI Buy", strategy.long)

if (sell_rsi_condition)
    strategy.entry("RSI Sell", strategy.short)

#ADD3 AND Use Candlestick Reversal Patterns in Conjunction with EMAs


doji = math.abs(open - close) <= (high - low) * 0.1

if (doji and buy_condition)
    strategy.entry("Doji Buy", strategy.long)

if (doji and sell_condition)
    strategy.entry("Doji Sell", strategy.short)

#ADD4 AND Incorporate Volume-Based Filters


volume_above_avg = volume > ta.sma(volume, 20)

if (buy_condition and volume_above_avg)
    strategy.entry("Volume Buy", strategy.long)

if (sell_condition and volume_above_avg)
    strategy.entry("Volume Sell", strategy.short)


#ADD5 AND Increase Signal Opportunities with Breakout Detection

breakout_length = input(20, title="Breakout Length")

breakout_buy = close > ta.highest(high, breakout_length)
breakout_sell = close < ta.lowest(low, breakout_length)

if (breakout_buy)
    strategy.entry("Breakout Buy", strategy.long)

if (breakout_sell)
    strategy.entry("Breakout Sell", strategy.short)


#ADD6 AND Use Divergence Detection (RSI vs Price)
    
bullish_divergence = ta.lowest(low, 5) < ta.lowest(low[1], 5) and rsi > rsi[1]
bearish_divergence = ta.highest(high, 5) > ta.highest(high[1], 5) and rsi < rsi[1]

if (bullish_divergence)
    strategy.entry("Divergence Buy", strategy.long)

if (bearish_divergence)
    strategy.entry("Divergence Sell", strategy.short)


#ADD7  Allow Partial Conditions to Trigger Trades


partial_buy_condition = ema10 > ema21 and ema21 > ema50
partial_sell_condition = ema10 < ema21 and ema21 < ema50

if (partial_buy_condition)
    strategy.entry("Partial Buy", strategy.long)

if (partial_sell_condition)
    strategy.entry("Partial Sell", strategy.short)

    #ADD8  Add Time-Based Entry Triggers


    trade_start = input.time(timestamp("0900"), title="Start Time")
trade_end = input.time(timestamp("1600"), title="End Time")

in_trade_session = time >= trade_start and time <= trade_end

if (buy_condition and in_trade_session)
    strategy.entry("Timed Buy", strategy.long)

if (sell_condition and in_trade_session)
    strategy.entry("Timed Sell", strategy.short)
