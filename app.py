import streamlit as st

# 防範瀏覽器自動翻譯導致 removeChild 崩潰錯誤
st.markdown("""
    <head>
        <meta name="google" content="notranslate">
    </head>
""", unsafe_allow_html=True)
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests

st.set_page_config(
    page_title="台股樂活五線譜與智慧選股",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 手機版 CSS
# =========================================================

st.markdown("""
<style>
.block-container {
    padding: 1rem 1rem 3rem 1rem;
    max-width: 1500px;
}

[data-testid="stMetricValue"] {
    font-size: clamp(1.1rem, 4vw, 2rem);
}

[data-testid="stDataFrame"] {
    font-size: 0.9rem;
}

@media (max-width: 768px) {

    .block-container {
        padding: .65rem .55rem 2rem .55rem;
    }

    h1 {
        font-size: 1.45rem !important;
    }

    h2 {
        font-size: 1.25rem !important;
    }

    h3 {
        font-size: 1.1rem !important;
    }

    .stButton button {
        min-height: 2.8rem;
        width: 100%;
    }

    .stSelectbox,
    .stSlider,
    .stRadio,
    .stTextInput,
    .stTextArea {
        font-size: .95rem;
    }

    [data-testid="stHorizontalBlock"] {
        gap: .45rem;
    }

    /* 手機：圖表與文字/按鈕拉開距離，避免上下滑動時誤觸圖表 */
    [data-testid="stPlotlyChart"] {
        margin: .75rem 0 1.25rem 0;
        padding: .35rem;
        border: 1px solid #D9D9D9;
        border-radius: 10px;
        background: #FFFFFF;
    }

    /* 手機上縮短圖表高度，減少單次滑動需要經過的圖表區域 */
    [data-testid="stPlotlyChart"] iframe {
        max-height: 480px;
    }
}

/* 桌面與手機都保留清楚的圖表外框 */
[data-testid="stPlotlyChart"] {
    border: 1px solid #D9D9D9;
    border-radius: 10px;
    padding: .25rem;
    background: #FFFFFF;
    box-sizing: border-box;
}
</style>
""", unsafe_allow_html=True)

st.title("📈 台股樂活五線譜與智慧選股系統")

FINMIND_DATA_URL = "https://api.finmindtrade.com/api/v4/data"

FINMIND_BRANCH_AGG_URL = (
    "https://api.finmindtrade.com/api/v4/"
    "taiwan_stock_trading_daily_report_secid_agg"
)


# =========================================================
# 常用台股清單
# =========================================================

DEFAULT_STOCKS_TEXT = """
2330,2454,2308,2317,3711,2881,2383,2303,2882,3037,2891,2382,2059,2345,2327,3017,6669,2885,2887,2886,2884,2880,2890,2892,2834,5880,2204,2357,2395,2408,2603,2609,2615,2912,1216,1301,1303,1326,6505,2002,3045,4904,2412,5876,2801,3231,2379,3653,3008,5274,2610,2618,2324,2353,2356,2377,2328,4938,2347,2449,2360,3443,6415,3661,3034,3035,2409,3481,6116,2371,1101,1102,1402,1504,1605,1717,1722,1802,1904,2105,2201,2542,2605,2606,2611,2809,2812,2838,2845,2851,2855,2867,2883,2888,2889,5871,6005,9904,9910,9921,9945,8454,2727,2915,5904,6592,6770,8046,6239,3189,4958,6213,6271,2439,2313,2368,3044,2367,5483,6488,3532,2455,2474,4961,3014,2376,2352,2354,4919,6269,3023,2421,1513,1519,1503,1609,1608,2014,2027,2013,5269,6414,8299,6223,3529,6147,8069,5347,3264,4174,1103,1104,1108,1210,1215,1217,1218,1227,1229,1231,1232,1233,1304,1305,1307,1308,1309,1310,1312,1313,1314,1315,1319,1321,1323,1409,1434,1440,1444,1447,1455,1476,1477,1507,1521,1522,1524,1525,1530,1532,1536,1537,1560,1582,1590,1611,1612,1615,1701,1702,1704,1707,1708,1710,1711,1712,1713,1714,1718,1720,1723,1726,1730,1732,1733,1736,1762,1773,1789,1795,1806,1808,1902,1905,1907,1909,2006,2009,2010,2012,2015,2017,2020,2022,2023,2028,2029,2030,2031,2032,2034,2038,2062,2101,2103,2104,2106,2108,2109,2114,2206,2207,2227,2231,2233,2239,2305,2312,2314,2316,2323,2329,2331,2332,2337,2338,2340,2342,2348,2349,2351,2355,2359,2362,2363,2364,2365,2373,2374,2375,2380,2385,2387,2388,2390,2392,2393,2397,2399,2401,2402,2404,2405,2406,2413,2414,2415,2417,2419,2420,2426,2427,2428,2430,2431,2433,2434,2436,2438,2440,2441,2442,2444,2450,2451,2453,2456,2457,2458,2459,2460,2461,2462,2464,2466,2467,2468,2471,2472,2476,2477,2478,2480,2481,2482,2483,2484,2485,2486,2488,2489,2492,2493,2495,2496,2497,2498,2501,2504,2505,2506,2509,2511,2514,2515,2516,2520,2524,2527,2528,2530,2534,2535,2536,2537,2538,2539,2540,2543,2545,2546,2547,2548,2597,2601,2607,2612,2613,2614,2616,2617,2630,2633,2634,2636,2637,2642,2701,2702,2704,2705,2706,2707,2712,2722,2723,2731,2739,2753,2816,2820,2832,2836,2841,2849,2850,2852,2897,2901,2903,2904,2905,2906,2908,2913,3002,3003,3004,3005,3006,3010,3011,3013,3015,3016,3018,3019,3021,3022,3024,3025,3026,3027,3028,3029,3030,3031,3032,3033,3036,3038,3040,3041,3042,3043,3046,3047,3048,3049,3050,3051,3052,3054,3055,3057,3058,3059,3060,3062,3090,3094,3130,3149,3164,3189,3209,3229,3231,3305,3308,3311,3312,3321,3338,3356,3376,3380,3406,3413,3450,3454,3481,3494,3501,3504,3515,3533,3535,3545,3550,3557,3576,3591,3593,3596
"""

DEFAULT_STOCKS = list(
    dict.fromkeys(
        [
            x.strip().upper().replace(".TW", "").replace(".TWO", "")
            for x in DEFAULT_STOCKS_TEXT.replace("\n", ",").split(",")
            if x.strip()
        ]
    )
)


# =========================================================
# 基本工具
# =========================================================

def normalize_code(value):
    return (
        str(value)
        .strip()
        .upper()
        .replace(".TW", "")
        .replace(".TWO", "")
    )


def nt(value):
    if value is None or pd.isna(value):
        return "—"
    return f"NT${float(value):,.2f}"


def api_headers(token):
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


# =========================================================
# FinMind：股票名稱
# =========================================================

@st.cache_data(ttl=86400, show_spinner=False)
def get_stock_info():

    response = requests.get(
        FINMIND_DATA_URL,
        params={
            "dataset": "TaiwanStockInfo"
        },
        timeout=30
    )

    response.raise_for_status()

    payload = response.json()

    if payload.get("status") not in (None, 200):
        raise RuntimeError(
            payload.get("msg", "FinMind 錯誤")
        )

    df = pd.DataFrame(
        payload.get("data", [])
    )

    if df.empty:
        return pd.DataFrame(
            columns=[
                "stock_id",
                "stock_name",
                "type",
                "date"
            ]
        )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["stock_id"] = (
        df["stock_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return (
        df
        .sort_values("date")
        .drop_duplicates(
            "stock_id",
            keep="last"
        )
    )


# =========================================================
# Yahoo Finance 股價
# =========================================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_yf_history(code, years):

    code = normalize_code(code)

    period = (
        f"{int(np.ceil(float(years)))}y"
    )

    for suffix in [".TW", ".TWO"]:

        try:

            df = yf.download(
                code + suffix,
                period=period,
                interval="1d",
                auto_adjust=False,
                progress=False,
                threads=False
            )

            if df is None or df.empty:
                continue

            if isinstance(
                df.columns,
                pd.MultiIndex
            ):
                df.columns = (
                    df.columns
                    .get_level_values(0)
                )

            columns = [
                "Open",
                "High",
                "Low",
                "Close",
                "Volume"
            ]

            if not all(
                c in df.columns
                for c in columns
            ):
                continue

            df = df[columns].copy()

            df.index = pd.to_datetime(
                df.index
            )

            if getattr(
                df.index,
                "tz",
                None
            ) is not None:
                df.index = (
                    df.index
                    .tz_localize(None)
                )

            df = df.dropna(
                subset=["Close"]
            )

            if not df.empty:
                return df

        except Exception:
            continue

    return pd.DataFrame()


# =========================================================
# 市值前500
# =========================================================

@st.cache_data(
    ttl=86400,
    show_spinner=False
)
def get_market_value_top500(token):

    if not token:
        return pd.DataFrame()

    end_date = (
        pd.Timestamp.today()
        .strftime("%Y-%m-%d")
    )

    start_date = (
        pd.Timestamp.today()
        - pd.Timedelta(days=10)
    ).strftime("%Y-%m-%d")

    response = requests.get(
        FINMIND_DATA_URL,
        headers=api_headers(token),
        params={
            "dataset":
                "TaiwanStockMarketValue",
            "start_date": start_date,
            "end_date": end_date
        },
        timeout=60
    )

    response.raise_for_status()

    payload = response.json()

    if payload.get("status") not in (None, 200):
        raise RuntimeError(
            payload.get(
                "msg",
                "市值資料錯誤"
            )
        )

    df = pd.DataFrame(
        payload.get("data", [])
    )

    if df.empty:
        return df

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["market_value"] = pd.to_numeric(
        df["market_value"],
        errors="coerce"
    )

    df["stock_id"] = (
        df["stock_id"]
        .astype(str)
        .str.zfill(4)
    )

    latest_date = df["date"].max()

    return (
        df[
            df["date"] == latest_date
        ]
        .dropna(
            subset=["market_value"]
        )
        .sort_values(
            "market_value",
            ascending=False
        )
        .drop_duplicates(
            "stock_id"
        )
        .head(500)
        .reset_index(drop=True)
    )


# =========================================================
# 三大法人
# =========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def get_institutional(
    code,
    start_date,
    end_date,
    token
):

    if not token:
        return pd.DataFrame()

    response = requests.get(
        FINMIND_DATA_URL,
        headers=api_headers(token),
        params={
            "dataset":
                "TaiwanStockInstitutionalInvestorsBuySellWide",
            "data_id": code,
            "start_date": start_date,
            "end_date": end_date
        },
        timeout=30
    )

    response.raise_for_status()

    payload = response.json()

    if payload.get("status") not in (None, 200):
        return pd.DataFrame()

    return pd.DataFrame(
        payload.get("data", [])
    )


# =========================================================
# 券商分點區間資料
# =========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def get_branch_agg(
    code,
    start_date,
    end_date,
    token
):

    if not token:
        return pd.DataFrame()

    response = requests.get(
        FINMIND_BRANCH_AGG_URL,
        headers=api_headers(token),
        params={
            "data_id": code,
            "start_date": start_date,
            "end_date": end_date
        },
        timeout=60
    )

    response.raise_for_status()

    payload = response.json()

    if payload.get("status") not in (None, 200):
        raise RuntimeError(
            payload.get(
                "msg",
                "券商分點資料錯誤"
            )
        )

    return pd.DataFrame(
        payload.get("data", [])
    )


# =========================================================
# 技術指標
# =========================================================

def indicators(df):

    x = df.copy()

    for n in [
        5,
        10,
        20,
        60,
        120,
        240
    ]:

        x[f"MA{n}"] = (
            x["Close"]
            .rolling(n)
            .mean()
        )

    # KD
    low9 = (
        x["Low"]
        .rolling(9)
        .min()
    )

    high9 = (
        x["High"]
        .rolling(9)
        .max()
    )

    denominator = (
        high9 - low9
    ).replace(0, np.nan)

    rsv = (
        (x["Close"] - low9)
        / denominator
        * 100
    )

    x["K"] = (
        rsv
        .ewm(
            com=2,
            adjust=False
        )
        .mean()
    )

    x["D"] = (
        x["K"]
        .ewm(
            com=2,
            adjust=False
        )
        .mean()
    )

    # MACD
    ema12 = (
        x["Close"]
        .ewm(
            span=12,
            adjust=False
        )
        .mean()
    )

    ema26 = (
        x["Close"]
        .ewm(
            span=26,
            adjust=False
        )
        .mean()
    )

    x["DIF"] = ema12 - ema26

    x["DEA"] = (
        x["DIF"]
        .ewm(
            span=9,
            adjust=False
        )
        .mean()
    )

    x["MACD_HIST"] = (
        x["DIF"] - x["DEA"]
    )

    # RSI
    delta = x["Close"].diff()

    gain = (
        delta
        .clip(lower=0)
        .rolling(14)
        .mean()
    )

    loss = (
        -delta
        .clip(upper=0)
        .rolling(14)
        .mean()
    )

    rs = (
        gain
        / loss.replace(0, np.nan)
    )

    x["RSI"] = (
        100
        - 100 / (1 + rs)
    )

    return x


# =========================================================
# 樂活五線譜
# =========================================================

def calculate_lohas(df, years):

    days = int(
        float(years) * 252
    )

    days = max(
        30,
        min(days, len(df))
    )

    data = (
        df
        .tail(days)
        .copy()
    )

    x = np.arange(
        len(data)
    )

    y = (
        data["Close"]
        .astype(float)
        .values
    )

    slope, intercept = np.polyfit(
        x,
        y,
        1
    )

    trend = (
        slope * x
        + intercept
    )

    std_dev = float(
        np.std(y - trend)
    )

    data["TL"] = trend
    data["EG"] = (
        trend + 2 * std_dev
    )
    data["G"] = (
        trend + std_dev
    )
    data["F"] = (
        trend - std_dev
    )
    data["EF"] = (
        trend - 2 * std_dev
    )

    return data


# =========================================================
# 型態辨識
# =========================================================

def detect_box_breakout(
    df,
    lookback,
    max_width,
    breakout_pct,
    volume_multiplier
):

    if len(df) < lookback + 5:
        return False

    recent = df.iloc[
        -lookback - 1:-1
    ]

    latest = df.iloc[-1]

    box_top = float(
        recent["High"].max()
    )

    box_bottom = float(
        recent["Low"].min()
    )

    if box_bottom <= 0:
        return False

    box_width = (
        box_top - box_bottom
    ) / box_bottom

    avg_volume = float(
        recent["Volume"]
        .tail(
            min(20, len(recent))
        )
        .mean()
    )

    if avg_volume <= 0:
        return False

    price_breakout = (
        float(latest["Close"])
        >= box_top
        * (1 + breakout_pct)
    )

    volume_breakout = (
        float(latest["Volume"])
        >= avg_volume
        * volume_multiplier
    )

    return (
        box_width <= max_width
        and price_breakout
        and volume_breakout
    )


def find_local_extrema(
    series,
    order=4
):

    values = (
        series
        .astype(float)
        .values
    )

    highs = []
    lows = []

    for i in range(
        order,
        len(values) - order
    ):

        if (
            values[i]
            >= max(
                values[
                    i - order:i
                ]
            )
            and
            values[i]
            >= max(
                values[
                    i + 1:i + order + 1
                ]
            )
        ):

            highs.append(i)

        if (
            values[i]
            <= min(
                values[
                    i - order:i
                ]
            )
            and
            values[i]
            <= min(
                values[
                    i + 1:i + order + 1
                ]
            )
        ):

            lows.append(i)

    return highs, lows


def detect_head_shoulders_bottom(
    df,
    shoulder_tolerance,
    head_depth,
    min_gap,
    neckline_break
):

    data = (
        df
        .tail(160)["Close"]
        .reset_index(drop=True)
    )

    if len(data) < 70:
        return False

    _, lows = find_local_extrema(
        data,
        order=4
    )

    if len(lows) < 3:
        return False

    for a, b, c in zip(
        lows[:-2],
        lows[1:-1],
        lows[2:]
    ):

        if (
            b - a < min_gap
            or
            c - b < min_gap
        ):
            continue

        left = float(data.iloc[a])
        head = float(data.iloc[b])
        right = float(data.iloc[c])

        shoulder_difference = (
            abs(left - right)
            / max(left, right)
        )

        if (
            shoulder_difference
            > shoulder_tolerance
        ):
            continue

        if (
            head
            >= min(left, right)
            * (1 - head_depth)
        ):
            continue

        left_neckline = float(
            data.iloc[a:b + 1].max()
        )

        right_neckline = float(
            data.iloc[b:c + 1].max()
        )

        neckline = max(
            left_neckline,
            right_neckline
        )

        current_price = float(
            data.iloc[-1]
        )

        if (
            current_price
            >= neckline
            * (1 + neckline_break)
        ):
            return True

    return False


def detect_head_shoulders_top(
    df,
    shoulder_tolerance,
    head_height,
    min_gap,
    neckline_break
):

    data = (
        df
        .tail(160)["Close"]
        .reset_index(drop=True)
    )

    if len(data) < 70:
        return False

    highs, _ = find_local_extrema(
        data,
        order=4
    )

    if len(highs) < 3:
        return False

    for a, b, c in zip(
        highs[:-2],
        highs[1:-1],
        highs[2:]
    ):

        if (
            b - a < min_gap
            or
            c - b < min_gap
        ):
            continue

        left = float(data.iloc[a])
        head = float(data.iloc[b])
        right = float(data.iloc[c])

        shoulder_difference = (
            abs(left - right)
            / max(left, right)
        )

        if (
            shoulder_difference
            > shoulder_tolerance
        ):
            continue

        if (
            head
            <= max(left, right)
            * (1 + head_height)
        ):
            continue

        left_neckline = float(
            data.iloc[a:b + 1].min()
        )

        right_neckline = float(
            data.iloc[b:c + 1].min()
        )

        neckline = min(
            left_neckline,
            right_neckline
        )

        current_price = float(
            data.iloc[-1]
        )

        if (
            current_price
            <= neckline
            * (1 - neckline_break)
        ):
            return True

    return False


# =========================================================
# 樂活五線譜圖
# =========================================================

def create_lohas_chart(data):

    fig = go.Figure()

    specifications = [
        (
            "EG",
            "極度貪婪",
            "#A12C7B",
            2
        ),
        (
            "G",
            "貪婪",
            "#E8A0BF",
            2
        ),
        (
            "TL",
            "趨勢線",
            "#707070",
            2
        ),
        (
            "F",
            "恐懼",
            "#5A9BD5",
            2
        ),
        (
            "EF",
            "極度恐懼",
            "#002060",
            2
        ),
        (
            "Close",
            "價格",
            "#000000",
            2.5
        )
    ]

    for column, name, color, width in specifications:

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data[column],
                mode="lines",
                name=name,
                line=dict(
                    color=color,
                    width=width
                )
            )
        )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        hovermode="x unified",
        dragmode=False,
        height=520,
        margin=dict(
            l=10,
            r=55,
            t=35,
            b=35
        ),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="#D9D9D9", width=1),
                fillcolor="rgba(0,0,0,0)"
            )
        ],
        legend=dict(
            orientation="h",
            y=1.03,
            x=0
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#EAEAEA",
        side="bottom",
        tickformat="%Y/%m/%d"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EAEAEA",
        side="right"
    )

    return fig


# =========================================================
# K線＋成交量＋MACD＋RSI
# =========================================================

def create_kline_chart(data):

    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.025,
        row_heights=[
            0.52,
            0.16,
            0.16,
            0.16
        ],
        subplot_titles=[
            "K線與均線",
            "成交量",
            "MACD",
            "RSI"
        ]
    )

    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="K線"
        ),
        row=1,
        col=1
    )

    moving_averages = [
        ("MA5", "#2196F3"),
        ("MA20", "#FF9800"),
        ("MA60", "#4CAF50"),
        ("MA120", "#E91E63"),
        ("MA240", "#9C27B0")
    ]

    for name, color in moving_averages:

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data[name],
                name=name,
                line=dict(
                    color=color,
                    width=1.4
                )
            ),
            row=1,
            col=1
        )

    volume_colors = np.where(
        data["Close"]
        >= data["Open"],
        "#E53935",
        "#43A047"
    )

    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["Volume"],
            name="成交量",
            marker_color=volume_colors
        ),
        row=2,
        col=1
    )

    macd_colors = np.where(
        data["MACD_HIST"] >= 0,
        "#E53935",
        "#43A047"
    )

    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["MACD_HIST"],
            name="MACD柱",
            marker_color=macd_colors
        ),
        row=3,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["DIF"],
            name="DIF",
            line=dict(
                color="#1565C0"
            )
        ),
        row=3,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["DEA"],
            name="DEA",
            line=dict(
                color="#EF6C00"
            )
        ),
        row=3,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["RSI"],
            name="RSI",
            line=dict(
                color="#8E24AA",
                width=2
            )
        ),
        row=4,
        col=1
    )

    fig.add_hline(
        y=70,
        line_dash="dot",
        row=4,
        col=1
    )

    fig.add_hline(
        y=30,
        line_dash="dot",
        row=4,
        col=1
    )

    fig.update_layout(
        height=820,
        paper_bgcolor="white",
        plot_bgcolor="white",
        hovermode="x unified",
        margin=dict(
            l=8,
            r=55,
            t=45,
            b=20
        ),
        legend=dict(
            orientation="h",
            y=1.02,
            x=0
        ),
        xaxis_rangeslider_visible=False
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#EAEAEA"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EAEAEA",
        side="right"
    )

    return fig


# =========================================================
# KD
# =========================================================

def create_kd_chart(data):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["K"],
            name="K",
            line=dict(
                color="#1565C0",
                width=2
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["D"],
            name="D",
            line=dict(
                color="#E91E63",
                width=2
            )
        )
    )

    fig.add_hline(
        y=80,
        line_dash="dot"
    )

    fig.add_hline(
        y=20,
        line_dash="dot"
    )

    fig.update_layout(
        height=280,
        paper_bgcolor="white",
        plot_bgcolor="white",
        hovermode="x unified",
        margin=dict(
            l=8,
            r=55,
            t=20,
            b=20
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#EAEAEA"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EAEAEA",
        side="right"
    )

    return fig


# =========================================================
# 主力／散戶圖
# =========================================================

def create_chip_chart(chip):

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=[
            "主力買賣超",
            "散戶買賣超（估算）"
        ]
    )

    main_colors = np.where(
        chip["Main"] >= 0,
        "#E53935",
        "#43A047"
    )

    retail_colors = np.where(
        chip["Retail"] >= 0,
        "#E53935",
        "#43A047"
    )

    fig.add_trace(
        go.Bar(
            x=chip["date"],
            y=chip["Main"],
            name="主力買賣超",
            marker_color=main_colors,
            hovertemplate=(
                "日期：%{x|%Y/%m/%d}"
                "<br>主力：%{y:,.0f} 張"
                "<extra></extra>"
            )
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=chip["date"],
            y=chip["MainCum"],
            name="主力累積",
            line=dict(
                color="#2E7D32",
                width=2
            ),
            hovertemplate=(
                "累計主力：%{y:,.0f} 張"
                "<extra></extra>"
            )
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Bar(
            x=chip["date"],
            y=chip["Retail"],
            name="散戶買賣超（估算）",
            marker_color=retail_colors,
            hovertemplate=(
                "日期：%{x|%Y/%m/%d}"
                "<br>散戶估算：%{y:,.0f} 張"
                "<extra></extra>"
            )
        ),
        row=2,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=chip["date"],
            y=chip["RetailCum"],
            name="散戶累積",
            line=dict(
                color="#EF9A9A",
                width=2
            ),
            hovertemplate=(
                "累計散戶：%{y:,.0f} 張"
                "<extra></extra>"
            )
        ),
        row=2,
        col=1
    )

    fig.update_layout(
        height=560,
        paper_bgcolor="white",
        plot_bgcolor="white",
        hovermode="x unified",
        margin=dict(
            l=8,
            r=55,
            t=50,
            b=20
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#EAEAEA"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EAEAEA",
        side="right"
    )

    return fig


# =========================================================
# 主力／散戶計算
# =========================================================

def build_chip_data(
    code,
    token,
    days=60,
    top_n=15
):

    if not token:
        return pd.DataFrame()

    end_date = pd.Timestamp.today()

    start_date = (
        end_date
        - pd.Timedelta(
            days=max(days * 2, 90)
        )
    )

    raw = get_branch_agg(
        code,
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"),
        token
    )

    if raw.empty:
        return pd.DataFrame()

    raw["buy_volume"] = pd.to_numeric(
        raw["buy_volume"],
        errors="coerce"
    ).fillna(0)

    raw["sell_volume"] = pd.to_numeric(
        raw["sell_volume"],
        errors="coerce"
    ).fillna(0)

    raw["date"] = pd.to_datetime(
        raw["date"],
        errors="coerce"
    )

    # FinMind 分點資料為股數，轉成張
    raw["net"] = (
        raw["buy_volume"]
        - raw["sell_volume"]
    ) / 1000.0

    result = []

    for date, daily in raw.groupby("date"):

        branches = (
            daily
            .groupby(
                [
                    "securities_trader_id",
                    "securities_trader"
                ],
                as_index=False
            )[
                [
                    "buy_volume",
                    "sell_volume",
                    "net"
                ]
            ]
        )

        top_buy = (
            branches
            .nlargest(
                top_n,
                "net"
            )
        )

        top_sell = (
            branches
            .nsmallest(
                top_n,
                "net"
            )
        )

        main_net = float(
            top_buy["net"].sum()
            + top_sell["net"].sum()
        )

        main_ids = set(
            top_buy[
                "securities_trader_id"
            ]
            .astype(str)
        )

        main_ids |= set(
            top_sell[
                "securities_trader_id"
            ]
            .astype(str)
        )

        retail_branches = branches[
            ~branches[
                "securities_trader_id"
            ]
            .astype(str)
            .isin(main_ids)
        ].copy()

        buy_count = int(
            (
                retail_branches[
                    "buy_volume"
                ] > 0
            ).sum()
        )

        sell_count = int(
            (
                retail_branches[
                    "sell_volume"
                ] > 0
            ).sum()
        )

        total_count = (
            buy_count
            + sell_count
        )

        retail_turnover = float(
            (
                retail_branches[
                    "buy_volume"
                ]
                + retail_branches[
                    "sell_volume"
                ]
            ).sum()
            / 1000.0
        )

        if total_count > 0:

            retail_net = (
                retail_turnover
                * (
                    buy_count
                    - sell_count
                )
                / total_count
                / 2.0
            )

        else:

            retail_net = 0.0

        result.append(
            {
                "date": date,
                "Main": main_net,
                "Retail": retail_net
            }
        )

    chip = (
        pd.DataFrame(result)
        .sort_values("date")
        .tail(days)
        .copy()
    )

    if chip.empty:
        return chip

    chip["MainCum"] = (
        chip["Main"]
        .cumsum()
    )

    chip["RetailCum"] = (
        chip["Retail"]
        .cumsum()
    )

    return chip


# =========================================================
# 讀取股票名稱
# =========================================================

try:
    stock_info = get_stock_info()
except Exception:
    stock_info = pd.DataFrame()

if not stock_info.empty:

    name_map = dict(
        zip(
            stock_info["stock_id"]
            .astype(str),
            stock_info["stock_name"]
            .astype(str)
        )
    )

else:

    name_map = {}


# =========================================================
# Sidebar
# =========================================================

st.sidebar.header("⚙️ 股票設定")

symbol = normalize_code(
    st.sidebar.text_input(
        "台股代號（不用輸入 .TW）",
        "2330"
    )
)

period_years = st.sidebar.select_slider(
    "📅 圖表觀察期間",
    options=[1, 2, 3, 4, 5],
    value=1,
    format_func=lambda x: f"{x} 年"
)

st.sidebar.caption("預設 1 年，可切換 2／3／4／5 年")

# 預設帶入你的 FinMind Token
MY_FINMIND_TOKEN = ""

finmind_token = st.sidebar.text_input(
    "FinMind Token (籌碼/市值前500需要)", 
    value=MY_FINMIND_TOKEN, 
    type="password"
)
stock_name = name_map.get(
    symbol,
    ""
)

st.sidebar.markdown("---")

st.sidebar.subheader(
    "📱 手機顯示"
)

mobile_mode = st.sidebar.checkbox(
    "手機最佳化模式",
    value=True
)


# =========================================================
# 分頁
# =========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 樂活五線譜",
        "📈 K線與指標",
        "🔍 智慧型態選股"
    ]
)


# =========================================================
# TAB 1：樂活五線譜
# =========================================================

with tab1:

    if not symbol:

        st.info(
            "請輸入台股代號"
        )

    else:

        df = get_yf_history(
            symbol,
            period_years
        )

        if df.empty:

            st.error(
                f"找不到 {symbol} 的台股資料，請確認代號。"
            )

        else:

            data = calculate_lohas(
                df,
                period_years
            )

            latest = data.iloc[-1]

            latest_price = float(
                latest["Close"]
            )

            if latest_price >= latest["EG"]:

                sentiment = "極度貪婪"

            elif latest_price >= latest["G"]:

                sentiment = "貪婪"

            elif latest_price <= latest["EF"]:

                sentiment = "極度恐懼"

            elif latest_price <= latest["F"]:

                sentiment = "恐懼"

            else:

                sentiment = "正常範圍"

            st.subheader(
                f"{symbol} {stock_name}".strip()
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "股票代碼",
                symbol
            )

            c2.metric(
                "最新價格",
                nt(latest_price)
            )

            c3.metric(
                "市場情緒",
                sentiment
            )

            st.plotly_chart(
                create_lohas_chart(data),
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                    "scrollZoom": False,
                    "doubleClick": False
                }
            )


# =========================================================
# TAB 2：K線與指標
# =========================================================

with tab2:

    if not symbol:

        st.info(
            "請輸入台股代號"
        )

    else:

        df = get_yf_history(
            symbol,
            period_years
        )

        if df.empty:

            st.error(
                f"找不到 {symbol} 的台股資料"
            )

        else:

            data = indicators(df)

            latest = data.iloc[-1]

            previous = (
                data.iloc[-2]
                if len(data) > 1
                else latest
            )

            st.subheader(
                f"{symbol} {stock_name}".strip()
            )

            change = (
                float(latest["Close"])
                - float(previous["Close"])
            )

            pct = (
                change
                / float(previous["Close"])
                * 100
                if float(previous["Close"]) != 0
                else 0
            )

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "最新價格",
                nt(latest["Close"]),
                f"{change:+.2f} ({pct:+.2f}%)"
            )

            c2.metric(
                "成交量",
                f"{int(latest['Volume']):,} 股"
            )

            c3.metric(
                "K / D",
                (
                    f"{latest['K']:.2f} / "
                    f"{latest['D']:.2f}"
                    if pd.notna(latest["K"])
                    and pd.notna(latest["D"])
                    else "—"
                )
            )

            c4.metric(
                "RSI",
                (
                    f"{latest['RSI']:.2f}"
                    if pd.notna(latest["RSI"])
                    else "—"
                )
            )

            st.plotly_chart(
                create_kline_chart(data),
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                    "scrollZoom": False,
                    "doubleClick": False
                }
            )

            st.subheader(
                "KD 指標"
            )

            st.plotly_chart(
                create_kd_chart(data),
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                    "scrollZoom": False,
                    "doubleClick": False
                }
            )

            # =================================================
            # 主力 vs 散戶
            # =================================================

            st.subheader(
                "主力 vs 散戶"
            )

            if not finmind_token:

                st.warning(
                    "未輸入 FinMind Token，因此不會用成交量自行猜測主力／散戶。"
                    "填入具券商分點資料權限的 Token 後才會顯示。"
                )

            else:

                try:

                    chip = build_chip_data(
                        symbol,
                        finmind_token,
                        days=60,
                        top_n=15
                    )

                    if chip.empty:

                        st.info(
                            "目前查不到此股票的券商分點資料，"
                            "或目前 Token 沒有分點資料權限。"
                        )

                    else:

                        latest_chip = chip.iloc[-1]

                        a, b, c = st.columns(3)

                        a.metric(
                            "今日主力買賣超",
                            f"{latest_chip['Main']:+,.0f} 張"
                        )

                        b.metric(
                            "今日散戶買賣超（估算）",
                            f"{latest_chip['Retail']:+,.0f} 張"
                        )

                        c.metric(
                            "主力累計",
                            f"{latest_chip['MainCum']:+,.0f} 張"
                        )

                        st.plotly_chart(
                            create_chip_chart(chip),
                            use_container_width=True,
                            config={
                                "displayModeBar": False,
                                "responsive": True
                            }
                        )

                        st.caption(
                            "主力：前15大買超分點與前15大賣超分點的淨買賣超。"
                            "散戶：依排除主力分點後的買賣家數與成交量推估，"
                            "不是直接辨識個別散戶帳戶。"
                        )

                except Exception as e:

                    st.error(
                        f"券商分點資料取得失敗：{e}"
                    )

            # =================================================
            # 三大法人
            # =================================================

            st.subheader(
                "三大法人"
            )

            if not finmind_token:

                st.info(
                    "填入 FinMind Token 後可顯示三大法人。"
                )

            else:

                try:

                    end_date = pd.Timestamp.today()

                    start_date = (
                        end_date
                        - pd.Timedelta(
                            days=int(
                                period_years
                                * 366
                            )
                        )
                    )

                    institutional = get_institutional(
                        symbol,
                        start_date.strftime(
                            "%Y-%m-%d"
                        ),
                        end_date.strftime(
                            "%Y-%m-%d"
                        ),
                        finmind_token
                    )

                    if not institutional.empty:

                        institutional["date"] = (
                            pd.to_datetime(
                                institutional["date"]
                            )
                        )

                        institutional = (
                            institutional
                            .set_index("date")
                        )

                        def net_column(
                            buy_column,
                            sell_column
                        ):

                            buy = pd.to_numeric(
                                institutional.get(
                                    buy_column,
                                    0
                                ),
                                errors="coerce"
                            ).fillna(0)

                            sell = pd.to_numeric(
                                institutional.get(
                                    sell_column,
                                    0
                                ),
                                errors="coerce"
                            ).fillna(0)

                            return (
                                buy - sell
                            ) / 1000

                        institutional["外資"] = (
                            net_column(
                                "Foreign_Investor_buy",
                                "Foreign_Investor_sell"
                            )
                        )

                        institutional["投信"] = (
                            net_column(
                                "Investment_Trust_buy",
                                "Investment_Trust_sell"
                            )
                        )

                        institutional["自營商"] = (
                            net_column(
                                "Dealer_self_buy",
                                "Dealer_self_sell"
                            )
                            + net_column(
                                "Dealer_Hedging_buy",
                                "Dealer_Hedging_sell"
                            )
                            + net_column(
                                "Dealer_buy",
                                "Dealer_sell"
                            )
                        )

                        fig = go.Figure()

                        for name, color in [
                            ("外資", "#1565C0"),
                            ("投信", "#E53935"),
                            ("自營商", "#43A047")
                        ]:

                            fig.add_trace(
                                go.Bar(
                                    x=institutional.index,
                                    y=institutional[name],
                                    name=name,
                                    marker_color=color
                                )
                            )

                        fig.update_layout(
                            barmode="group",
                            height=380,
                            paper_bgcolor="white",
                            plot_bgcolor="white",
                            hovermode="x unified",
                            margin=dict(
                                l=8,
                                r=55,
                                t=25,
                                b=20
                            )
                        )

                        fig.update_yaxes(
                            side="right",
                            title="張"
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True,
                            config={
                                "displayModeBar": False,
                                "responsive": True
                            }
                        )

                    else:

                        st.info(
                            "查無三大法人資料"
                        )

                except Exception as e:

                    st.warning(
                        f"三大法人資料暫時無法取得：{e}"
                    )


# =========================================================
# TAB 3：智慧型態選股
# =========================================================

with tab3:

    st.subheader(
        "🔍 智慧型態選股"
    )

    pattern = st.radio(
        "型態",
        [
            "突破區間整理（箱型突破）",
            "頭肩底（買入訊號）",
            "頭肩頂（賣出訊號）"
        ],
        horizontal=True
    )

    universe = st.radio(
        "掃描範圍",
        [
            "常用個股管理",
            "市值前500大",
            "自訂台股清單"
        ],
        horizontal=True
    )

    # =====================================================
    # 常用個股
    # =====================================================

    if universe == "常用個股管理":

        stock_text = st.text_area(
            "常用個股管理（全部保留）",
            value=", ".join(
                DEFAULT_STOCKS
            ),
            height=150
        )

        watchlist = list(
            dict.fromkeys(
                [
                    normalize_code(x)
                    for x in stock_text.split(",")
                    if normalize_code(x)
                ]
            )
        )

    # =====================================================
    # 自訂清單
    # =====================================================

    elif universe == "自訂台股清單":

        stock_text = st.text_area(
            "台股代號清單",
            value=", ".join(
                DEFAULT_STOCKS[:60]
            ),
            height=150
        )

        watchlist = list(
            dict.fromkeys(
                [
                    normalize_code(x)
                    for x in stock_text.split(",")
                    if normalize_code(x)
                ]
            )
        )

    # =====================================================
    # 市值前500
    # =====================================================

    else:

        watchlist = []

        if not finmind_token:

            st.warning(
                "市值前500需要 FinMind Token。"
            )

        else:

            try:

                market_value = (
                    get_market_value_top500(
                        finmind_token
                    )
                )

                if not market_value.empty:

                    watchlist = (
                        market_value["stock_id"]
                        .astype(str)
                        .str.zfill(4)
                        .tolist()
                    )

                    st.success(
                        f"取得 {len(watchlist)} 檔市值前500大標的；"
                        f"資料日："
                        f"{market_value['date'].max().strftime('%Y-%m-%d')}"
                    )

                else:

                    st.warning(
                        "無法取得市值前500資料，"
                        "請確認 Token 的會員權限。"
                    )

            except Exception as e:

                st.error(
                    f"市值前500取得失敗：{e}"
                )

    # =====================================================
    # 選股強度
    # =====================================================

    st.markdown(
        "### 🎯 選股強度"
    )

    strength = st.select_slider(
        "快速調整",
        options=[
            "寬鬆",
            "標準",
            "嚴格",
            "極嚴格"
        ],
        value="嚴格"
    )

    presets = {

        "寬鬆": {
            "box_days": 20,
            "box_width": 0.20,
            "breakout": 0.005,
            "volume": 1.00,
            "shoulder": 0.12,
            "head": 0.03,
            "gap": 4,
            "neck": 0.00
        },

        "標準": {
            "box_days": 30,
            "box_width": 0.15,
            "breakout": 0.010,
            "volume": 1.10,
            "shoulder": 0.08,
            "head": 0.04,
            "gap": 5,
            "neck": 0.005
        },

        "嚴格": {
            "box_days": 40,
            "box_width": 0.10,
            "breakout": 0.020,
            "volume": 1.30,
            "shoulder": 0.06,
            "head": 0.06,
            "gap": 7,
            "neck": 0.010
        },

        "極嚴格": {
            "box_days": 60,
            "box_width": 0.08,
            "breakout": 0.030,
            "volume": 1.50,
            "shoulder": 0.04,
            "head": 0.08,
            "gap": 10,
            "neck": 0.020
        }
    }

    preset = presets[strength]

    # =====================================================
    # 進階參數
    # =====================================================

    with st.expander(
        "⚙️ 進階參數（可以自行微調）",
        expanded=False
    ):

        box_days = st.slider(
            "箱型整理天數",
            10,
            90,
            preset["box_days"],
            5
        )

        box_width = st.slider(
            "箱型最大振幅",
            0.05,
            0.30,
            preset["box_width"],
            0.01,
            format="%.0f%%"
        )

        breakout = st.slider(
            "突破幅度",
            0.0,
            0.10,
            preset["breakout"],
            0.005,
            format="%.1f%%"
        )

        volume_multiplier = st.slider(
            "成交量放大倍數",
            0.8,
            3.0,
            preset["volume"],
            0.1,
            format="%.1fx"
        )

        shoulder_tolerance = st.slider(
            "左右肩最大差異",
            0.02,
            0.20,
            preset["shoulder"],
            0.01,
            format="%.0f%%"
        )

        head_depth = st.slider(
            "頭部至少超過／低於肩膀",
            0.02,
            0.20,
            preset["head"],
            0.01,
            format="%.0f%%"
        )

        min_gap = st.slider(
            "左右肩／頭最小間隔",
            3,
            30,
            preset["gap"],
            1
        )

        neckline_break = st.slider(
            "頸線突破／跌破幅度",
            0.0,
            0.10,
            preset["neck"],
            0.005,
            format="%.1f%%"
        )

    scan_years = st.select_slider(
        "型態掃描資料",
        options=[
            0.5,
            1.0,
            1.5,
            2.0
        ],
        value=1.0
    )

    # =====================================================
    # 開始掃描
    # =====================================================

    if st.button(
        "🚀 開始型態掃描",
        type="primary"
    ):

        if not watchlist:

            st.error(
                "沒有可掃描的股票"
            )

        else:

            results = []

            failed = 0

            progress = st.progress(
                0,
                text="正在掃描…"
            )

            for index, ticker in enumerate(
                watchlist
            ):

                try:

                    data = get_yf_history(
                        ticker,
                        scan_years
                    )

                    minimum_length = max(
                        70,
                        box_days + 5
                    )

                    if len(data) >= minimum_length:

                        if pattern.startswith(
                            "突破"
                        ):

                            matched = (
                                detect_box_breakout(
                                    data,
                                    box_days,
                                    box_width,
                                    breakout,
                                    volume_multiplier
                                )
                            )

                        elif pattern.startswith(
                            "頭肩底"
                        ):

                            matched = (
                                detect_head_shoulders_bottom(
                                    data,
                                    shoulder_tolerance,
                                    head_depth,
                                    min_gap,
                                    neckline_break
                                )
                            )

                        else:

                            matched = (
                                detect_head_shoulders_top(
                                    data,
                                    shoulder_tolerance,
                                    head_depth,
                                    min_gap,
                                    neckline_break
                                )
                            )

                        if matched:

                            latest_price = float(
                                data["Close"].iloc[-1]
                            )

                            results.append(
                                {
                                    "代號": ticker,
                                    "股票名稱":
                                        name_map.get(
                                            ticker,
                                            "—"
                                        ),
                                    "最新價格":
                                        nt(
                                            latest_price
                                        ),
                                    "日期":
                                        data.index[-1]
                                        .strftime(
                                            "%Y/%m/%d"
                                        )
                                }
                            )

                except Exception:

                    failed += 1

                progress.progress(
                    (index + 1)
                    / len(watchlist),
                    text=(
                        f"正在掃描 "
                        f"{index + 1}/"
                        f"{len(watchlist)}"
                    )
                )

            progress.empty()

            if results:

                st.success(
                    f"找到 {len(results)} 檔符合"
                    f"「{pattern}」；"
                    f"強度：{strength}"
                )

                st.dataframe(
                    pd.DataFrame(results),
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "目前沒有符合條件的標的。"
                    "可以把強度調成「寬鬆」，"
                    "或在進階參數放寬條件。"
                )

            if failed:

                st.caption(
                    f"有 {failed} 檔資料取得失敗，"
                    "已自動略過。"
                )