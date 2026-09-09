import warnings
warnings.filterwarnings("ignore")

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import streamlit as st
import yfinance as yf
from scipy.signal import argrelextrema

# ============================================================
# 樂活五線譜與智慧選股系統
# ============================================================

st.set_page_config(
    page_title="樂活五線譜與智慧選股系統",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@media (max-width: 768px) {
    .block-container {
        padding: .65rem .55rem 1.5rem .55rem;
    }

    h1 {
        font-size: 1.55rem !important;
    }

    h2 {
        font-size: 1.25rem !important;
    }

    h3 {
        font-size: 1.05rem !important;
    }

    .stButton > button {
        width: 100%;
        min-height: 2.6rem;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: .82rem;
        padding: 0 .45rem;
    }

    div[data-testid="stMetric"] {
        padding: .4rem .2rem;
    }
}
</style>
""", unsafe_allow_html=True)

FINMIND_API = "https://api.finmindtrade.com/api/v4/data"

# ============================================================
# 常用股票清單
# ============================================================

COMMON_STOCKS_TEXT = """
2330 2454 2308 2317 3711 2881 2383 2303 2882 3037 2891 2382 2059 2345
2327 3017 6669 2885 2887 2886 2884 2880 2890 2892 2834 5880 2204 2357
2395 2408 2603 2609 2615 2912 1216 1301 1303 1326 6505 2002 3045 4904
2412 5876 2801 3231 2379 3653 3008 5274 2610 2618 2324 2353 2356 2377
2328 4938 2347 2449 2360 3443 6415 2376 2385 2392 2404 2409 2439 2474
2481 2492 2498 2605 2617 2727 2823 2883 2888 2897 2915 3005 3034 3036
3035 3044 3090 3167 3406 3702 3706 3707 3711 3714 4938 4961 5269 5278
5871 5876 6239 6414 6488 8046 2352 2354 2356 2357 2359 2362 2367 2368
2376 2382 2385 2387 2393 2401 2402 2408 2412 2421 2423 2436 2439 2441
2442 2449 2451 2454 2458 2474 2476 2480 2481 2485 2492 2498 2501 2504
2505 2506 2515 2520 2524 2528 2534 2535 2536 2537 2540 2542 2543 2545
2546 2547 2548 2597 2601 2603 2605 2606 2607 2608 2610 2611 2612 2613
2615 2617 2618 2637 2642 2701 2702 2722 2723 2727 2801 2809 2812 2820
2823 2834 2836 2838 2845 2849 2850 2851 2852 2855 2867 2880 2881 2882
2883 2884 2885 2886 2887 2888 2889 2890 2891 2892 2897 2903 2912 2913
2915 3002 3003 3004 3005 3006 3008 3010 3014 3015 3016 3017 3019 3022
3023 3024 3025 3026 3027 3028 3029 3030 3031 3032 3033 3034 3035 3036
3037 3038 3042 3044 3045 3046 3047 3048 3049 3051 3054 3055 3056 3057
3058 3059 3060 3062 3090 3167 3231 3305 3406 3443 3501 3530 3532 3653
3661 3702 3706 3707 3711 3712 3714 4904 4906 4915 4919 4938 4942 4958
4960 4961 4977 4989 4994 5258 5269 5274 5278 5347 5484 5536 5607 5871
5876 5880 6120 6239 6414 6415 6456 6477 6488 6505 6515 6669 6690 6770
8046 8112 8210 9904 9910 9914 9921 9938 9941 9945 9946 9940 9941
1301 1303 1304 1305 1307 1308 1309 1310 1312 1313 1314 1315 1316 1319
1321 1323 1324 1325 1326 1337 1402 1409 1410 1414 1434 1436 1440 1444
1445 1447 1451 1452 1455 1457 1459 1460 1463 1464 1465 1466 1467 1470
1471 1472 1473 1474 1475 1476 1477 1503 1504 1507 1513 1514 1515 1516
1517 1519 1521 1522 1524 1525 1527 1528 1529 1530 1531 1532 1533
1535 1536 1537 1538 1539 1540 1541 1558 1560 1563 1565 1568 1580 1582
1603 1604 1605 1608 1609 1611 1612 1614 1615 1616 1617 1618 1626 1702
1707 1708 1710 1711 1712 1713 1714 1717 1718 1720 1721 1722 1723 1724
1725 1726 1727 1730 1731 1732 1733 1734 1735 1736 1737 1762 1773 1776
1783 1785 1786 1789 1795 1802 1805 1806 1808 1809 1810 1817 1904 1905
1907 1909 2002 2006 2007 2008 2010 2012 2013 2014 2015 2017 2020 2022
2023 2024 2025 2027 2028 2029 2030 2031 2032 2033 2034 2038 2049 2059
2101 2102 2103 2104 2105 2106 2107 2108 2109 2114 2201 2204 2206 2207
2208 2211 2227 2228 2231 2233 2236 2239 2243 2301 2302 2303 2305 2308
2312 2313 2316 2317 2323 2324 2327 2328 2329 2330 2331 2332 2337 2338
2340 2342 2344 2345 2347 2348 2349 2351 2352 2353 2354 2355 2356 2357
2359 2360 2362 2363 2364 2365 2367 2368 2369 2371 2373 2374 2375 2376
2377 2379 2380 2382 2383 2385 2387 2388 2390 2392 2393 2395 2397 2399
2401 2402 2404 2405 2406 2408 2409 2412 2413 2414 2415 2417 2419 2420
2421 2423 2424 2425 2426 2427 2428 2429 2430 2431 2433 2434 2436 2438
2439 2440 2441 2442 2443 2444 2449 2450 2451 2453 2454 2455 2457 2458
2459 2460 2461 2462 2464 2465 2466 2467 2468 2471 2472 2474 2476 2477
2478 2480 2481 2482 2483 2484 2485 2486 2488 2489 2491 2492 2493 2495
2496 2497 2498 2501 2504 2505 2506 2509 2511 2514 2515 2516 2520 2524
2527 2528 2530 2534 2535 2536 2537 2538 2540 2542 2543 2545 2546 2547
2548 2597 2601 2603 2605 2606 2607 2608 2610 2611 2612 2613 2614 2615
2616 2617 2618 2630 2633 2634 2636 2637 2640 2701 2702 2704 2705 2706
2707 2712 2722 2723 2727 2729 2731 2739 2748 2801 2809 2812 2820 2823
2834 2836 2838 2845 2849 2850 2851 2852 2855 2867 2880 2881 2882 2883
2884 2885 2886 2887 2888 2889 2890 2891 2892 2897 2903 2904 2905 2906
2908 2910 2911 2912 2913 2915 3002 3003 3004 3005 3006 3008 3010 3013
3014 3015 3016 3017 3018 3019 3021 3022 3023 3024 3025 3026 3027 3028
3029 3030 3031 3032 3033 3034 3035 3036 3037 3038 3040 3041 3042 3044
3045 3046 3047 3048 3049 3051 3054 3055 3056 3057 3058 3059 3060 3090
3167 3231 3305 3406 3443 3501 3530 3532 3653 3661 3702 3706 3707 3711
3714 4904 4906 4915 4919 4938 4942 4958 4960 4961 4977 4989 4994 5258
5269 5274 5278 5347 5484 5536 5607 5871 5876 5880 6120 6239 6414 6415
6456 6477 6488 6505 6515 6669 6690 6770 8046 8112 8210 9904 9910 9914
9921 9938 9941 9945 9946
"""

COMMON_STOCKS = sorted(
    set(x for x in COMMON_STOCKS_TEXT.split() if x.isdigit())
)

# ============================================================
# 四級篩選條件
#
# 「嚴格」完全以這次使用者提供的新版條件為核心：
# 箱型 60 日 / 振幅 <20% / 突破 0~5% / 量 >1.3倍
# 頭肩型態：至少60日 / 右肩最近20日 / 左右肩差 <10%
#
# 其他三級以此為中心向外／向內調整。
# ============================================================

PRESETS = {
    "寬鬆": {
        "box_days": 30,
        "box_width": 0.25,
        "breakout_pct": 0.08,
        "vol_mult": 1.10,
        "shoulder_diff": 0.15,
        "right_window": 30,
        "neckline_buffer": 0.04,
    },
    "標準": {
        "box_days": 45,
        "box_width": 0.22,
        "breakout_pct": 0.06,
        "vol_mult": 1.20,
        "shoulder_diff": 0.12,
        "right_window": 25,
        "neckline_buffer": 0.03,
    },
    "嚴格": {
        "box_days": 60,
        "box_width": 0.20,
        "breakout_pct": 0.05,
        "vol_mult": 1.30,
        "shoulder_diff": 0.10,
        "right_window": 20,
        "neckline_buffer": 0.02,
    },
    "極嚴格": {
        "box_days": 75,
        "box_width": 0.12,
        "breakout_pct": 0.03,
        "vol_mult": 1.50,
        "shoulder_diff": 0.06,
        "right_window": 15,
        "neckline_buffer": 0.01,
    },
}


# ============================================================
# 基本工具
# ============================================================

def normalize_code(code):
    return (
        str(code)
        .strip()
        .upper()
        .replace(".TW", "")
        .replace(".TWO", "")
    )


@st.cache_data(ttl=86400, show_spinner=False)
def get_stock_names():
    try:
        response = requests.get(
            FINMIND_API,
            params={
                "dataset": "TaiwanStockInfo",
                "start_date": "2020-01-01",
            },
            timeout=20,
        )
        response.raise_for_status()

        df = pd.DataFrame(response.json().get("data", []))

        if df.empty:
            return {}

        if "stock_id" not in df.columns or "stock_name" not in df.columns:
            return {}

        if "date" in df.columns:
            df["date"] = pd.to_datetime(
                df["date"],
                errors="coerce",
            )
            df = df.sort_values("date")

        df = df.drop_duplicates(
            "stock_id",
            keep="last",
        )

        return dict(
            zip(
                df["stock_id"].astype(str),
                df["stock_name"].astype(str),
            )
        )

    except Exception:
        return {}


def get_stock_name(code):
    return get_stock_names().get(
        normalize_code(code),
        "",
    )


# ============================================================
# Yahoo Finance
# ============================================================

@st.cache_data(ttl=900, show_spinner=False)
def get_history(code, years=3.5):
    code = normalize_code(code)

    period = (
        f"{max(1.0, float(years) + 0.5):.1f}y"
    )

    for suffix in (".TW", ".TWO"):
        try:
            df = yf.Ticker(
                code + suffix
            ).history(
                period=period,
                interval="1d",
                auto_adjust=False,
                actions=False,
            )

            if df is None or df.empty:
                continue

            if isinstance(
                df.columns,
                pd.MultiIndex,
            ):
                df.columns = (
                    df.columns
                    .get_level_values(0)
                )

            required = [
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
            ]

            if not all(
                c in df.columns
                for c in required
            ):
                continue

            df = (
                df[required]
                .copy()
                .dropna(
                    subset=[
                        "High",
                        "Low",
                        "Close",
                    ]
                )
            )

            df.index = pd.to_datetime(
                df.index
            )

            return df

        except Exception:
            continue

    return pd.DataFrame()


# ============================================================
# 樂活五線譜
# ============================================================

def calculate_lohas(df, years):
    n = int(
        float(years) * 252
    )

    work = df.tail(n).copy()

    if len(work) < 30:
        return pd.DataFrame()

    y = (
        work["Close"]
        .astype(float)
        .to_numpy()
    )

    x = np.arange(
        len(y),
        dtype=float,
    )

    slope, intercept = np.polyfit(
        x,
        y,
        1,
    )

    trend = (
        slope * x
        + intercept
    )

    std = float(
        np.std(
            y - trend,
            ddof=1,
        )
    )

    result = pd.DataFrame(
        index=work.index
    )

    result["Close"] = y
    result["極度貪婪"] = (
        trend + 2 * std
    )
    result["貪婪"] = (
        trend + std
    )
    result["趨勢線"] = trend
    result["恐懼"] = (
        trend - std
    )
    result["極度恐懼"] = (
        trend - 2 * std
    )

    return result


# ============================================================
# 頭肩頂
# 賣出／避險預警
# ============================================================

def detect_head_and_shoulders_top(
    df,
    order=5,
    right_window=20,
    shoulder_diff_limit=0.10,
    neckline_lower=0.85,
    neckline_upper=1.02,
):
    if len(df) < 60:
        return False, None

    prices = (
        df["High"]
        .astype(float)
        .to_numpy()
    )

    max_idx = argrelextrema(
        prices,
        np.greater,
        order=order,
    )[0]

    if len(max_idx) < 3:
        return False, None

    h1, h2, h3 = max_idx[-3:]

    # 右肩必須在最近 N 個交易日
    if (
        len(df) - 1 - h3
        > right_window
    ):
        return False, None

    p1 = prices[h1]
    p2 = prices[h2]
    p3 = prices[h3]

    # 頭部高於左右肩
    if not (
        p2 > p1
        and p2 > p3
    ):
        return False, None

    if min(p1, p3) <= 0:
        return False, None

    shoulder_diff = (
        abs(p1 - p3)
        / min(p1, p3)
    )

    # 左右肩高度不能差太多
    if (
        shoulder_diff
        >= shoulder_diff_limit
    ):
        return False, None

    if h3 <= h1 + 1:
        return False, None

    lows_between = (
        df["Low"]
        .iloc[h1:h3 + 1]
        .astype(float)
    )

    if lows_between.empty:
        return False, None

    neckline = float(
        lows_between.min()
    )

    latest_close = float(
        df["Close"].iloc[-1]
    )

    # 股價位於頸線附近
    if not (
        neckline * neckline_lower
        <= latest_close
        <= neckline * neckline_upper
    ):
        return False, None

    # 右肩量小於頭部量
    vol_h2 = float(
        df["Volume"]
        .iloc[
            max(0, h2 - 2):h2 + 3
        ]
        .mean()
    )

    vol_h3 = float(
        df["Volume"]
        .iloc[
            max(0, h3 - 2):h3 + 3
        ]
        .mean()
    )

    if (
        vol_h2 <= 0
        or vol_h3 >= vol_h2
    ):
        return False, None

    return True, {
        "left_shoulder": (
            df.index[h1],
            p1,
        ),
        "head": (
            df.index[h2],
            p2,
        ),
        "right_shoulder": (
            df.index[h3],
            p3,
        ),
        "neckline": neckline,
    }


# ============================================================
# 頭肩底
# 買進／起漲訊號
# ============================================================

def detect_head_and_shoulders_bottom(
    df,
    order=5,
    right_window=20,
    shoulder_diff_limit=0.10,
    neckline_lower=0.98,
    neckline_upper=1.08,
):
    if len(df) < 60:
        return False, None

    prices = (
        df["Low"]
        .astype(float)
        .to_numpy()
    )

    min_idx = argrelextrema(
        prices,
        np.less,
        order=order,
    )[0]

    if len(min_idx) < 3:
        return False, None

    l1, l2, l3 = min_idx[-3:]

    # 右底必須在最近 N 個交易日
    if (
        len(df) - 1 - l3
        > right_window
    ):
        return False, None

    p1 = prices[l1]
    p2 = prices[l2]
    p3 = prices[l3]

    # 頭部低於左右肩
    if not (
        p2 < p1
        and p2 < p3
    ):
        return False, None

    if min(p1, p3) <= 0:
        return False, None

    shoulder_diff = (
        abs(p1 - p3)
        / min(p1, p3)
    )

    if (
        shoulder_diff
        >= shoulder_diff_limit
    ):
        return False, None

    if l3 <= l1 + 1:
        return False, None

    highs_between = (
        df["High"]
        .iloc[l1:l3 + 1]
        .astype(float)
    )

    if highs_between.empty:
        return False, None

    neckline = float(
        highs_between.max()
    )

    latest_close = float(
        df["Close"].iloc[-1]
    )

    # 突破／回測頸線附近
    if not (
        neckline * neckline_lower
        <= latest_close
        <= neckline * neckline_upper
    ):
        return False, None

    return True, {
        "left_shoulder": (
            df.index[l1],
            p1,
        ),
        "head": (
            df.index[l2],
            p2,
        ),
        "right_shoulder": (
            df.index[l3],
            p3,
        ),
        "neckline": neckline,
    }


# ============================================================
# 箱型突破
# 帶量起漲點
# ============================================================

def detect_box_breakout(
    df,
    box_days=60,
    max_width=0.20,
    breakout_max=0.05,
    vol_mult=1.30,
):
    if len(df) < box_days + 1:
        return False, None

    # 不把今天算進箱體
    past = df.iloc[
        -(box_days + 1):-1
    ]

    if past.empty:
        return False, None

    box_max = float(
        past["High"].max()
    )

    box_min = float(
        past["Low"].min()
    )

    if box_min <= 0:
        return False, None

    amplitude = (
        box_max - box_min
    ) / box_min

    latest_close = float(
        df["Close"].iloc[-1]
    )

    prev_close = float(
        df["Close"].iloc[-2]
    )

    # 箱體振幅限制
    if amplitude >= max_width:
        return False, None

    # 昨天尚在箱內，今天剛突破箱頂
    if not (
        prev_close <= box_max
        and box_max < latest_close
        <= box_max * (1 + breakout_max)
    ):
        return False, None

    # 今日成交量 > 前20日均量指定倍數
    vol_ma20 = float(
        df["Volume"]
        .iloc[-21:-1]
        .mean()
    )

    latest_vol = float(
        df["Volume"].iloc[-1]
    )

    if (
        vol_ma20 <= 0
        or latest_vol
        <= vol_ma20 * vol_mult
    ):
        return False, None

    return True, {
        "box_max": box_max,
        "box_min": box_min,
        "breakout_price": latest_close,
        "amplitude": amplitude,
        "volume_ratio": (
            latest_vol / vol_ma20
        ),
    }


# ============================================================
# 技術指標
# ============================================================

def add_indicators(df):
    result = df.copy()

    close = (
        result["Close"]
        .astype(float)
    )

    # 均線
    for n in (
        5,
        20,
        60,
        120,
        240,
    ):
        result[f"MA{n}"] = (
            close.rolling(n).mean()
        )

    # MACD
    ema12 = close.ewm(
        span=12,
        adjust=False,
    ).mean()

    ema26 = close.ewm(
        span=26,
        adjust=False,
    ).mean()

    result["DIF"] = (
        ema12 - ema26
    )

    result["MACD"] = (
        result["DIF"]
        .ewm(
            span=9,
            adjust=False,
        )
        .mean()
    )

    result["MACD_HIST"] = (
        result["DIF"]
        - result["MACD"]
    )

    # RSI
    delta = close.diff()

    gain = (
        delta.clip(lower=0)
        .rolling(14)
        .mean()
    )

    loss = (
        -delta.clip(upper=0)
        .rolling(14)
        .mean()
    )

    rs = (
        gain
        / loss.replace(
            0,
            np.nan,
        )
    )

    result["RSI"] = (
        100
        - 100 / (1 + rs)
    )

    # KD
    low9 = (
        result["Low"]
        .rolling(9)
        .min()
    )

    high9 = (
        result["High"]
        .rolling(9)
        .max()
    )

    denominator = (
        high9 - low9
    ).replace(
        0,
        np.nan,
    )

    rsv = (
        (close - low9)
        / denominator
        * 100
    )

    result["K"] = (
        rsv.ewm(
            com=2,
            adjust=False,
        ).mean()
    )

    result["D"] = (
        result["K"]
        .ewm(
            com=2,
            adjust=False,
        ).mean()
    )

    return result


# ============================================================
# FinMind
# ============================================================

def auth_headers(token):
    if token:
        return {
            "Authorization": f"Bearer {token}"
        }
    return {}


@st.cache_data(
    ttl=3600,
    show_spinner=False,
)
def get_branch_agg(
    code,
    start_date,
    end_date,
    token,
):
    if not token:
        return pd.DataFrame()

    try:
        response = requests.get(
            FINMIND_API,
            headers=auth_headers(token),
            params={
                "dataset":
                    "TaiwanStockTradingDailyReportSecIdAgg",
                "data_id":
                    normalize_code(code),
                "start_date":
                    start_date,
                "end_date":
                    end_date,
            },
            timeout=30,
        )

        response.raise_for_status()

        return pd.DataFrame(
            response.json().get(
                "data",
                [],
            )
        )

    except Exception:
        return pd.DataFrame()


def calculate_main_retail(
    branch_df,
):
    if (
        branch_df.empty
        or "date"
        not in branch_df.columns
    ):
        return pd.DataFrame()

    df = branch_df.copy()

    for col in (
        "buy_volume",
        "sell_volume",
    ):
        if col not in df.columns:
            return pd.DataFrame()

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce",
        ).fillna(0)

    df["net"] = (
        df["buy_volume"]
        - df["sell_volume"]
    )

    rows = []

    for date, day in df.groupby(
        "date"
    ):
        top_buy = day.nlargest(
            15,
            "net",
        )

        top_sell = day.nsmallest(
            15,
            "net",
        )

        selected = set(
            top_buy.index
        ) | set(
            top_sell.index
        )

        if selected:
            main_net = float(
                day.loc[
                    list(selected),
                    "net",
                ].sum()
            )
        else:
            main_net = 0.0

        remain = day.drop(
            index=list(selected),
            errors="ignore",
        )

        if remain.empty:
            retail_net = 0.0
        else:
            retail_net = float(
                remain["net"].sum()
            )

        rows.append(
            {
                "date":
                    pd.to_datetime(date),
                "Main":
                    main_net / 1000,
                "Retail":
                    retail_net / 1000,
            }
        )

    result = pd.DataFrame(
        rows
    ).sort_values("date")

    if result.empty:
        return result

    result["MainCum"] = (
        result["Main"].cumsum()
    )

    result["RetailCum"] = (
        result["Retail"].cumsum()
    )

    return result


# ============================================================
# 三大法人
# ============================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False,
)
def get_institutional(
    code,
    start_date,
    end_date,
):
    try:
        response = requests.get(
            FINMIND_API,
            params={
                "dataset":
                    "TaiwanStockInstitutionalInvestorsBuySellWide",
                "data_id":
                    normalize_code(code),
                "start_date":
                    start_date,
                "end_date":
                    end_date,
            },
            timeout=30,
        )

        response.raise_for_status()

        return pd.DataFrame(
            response.json().get(
                "data",
                [],
            )
        )

    except Exception:
        return pd.DataFrame()


def prepare_institutional(
    df,
):
    if (
        df.empty
        or "date"
        not in df.columns
    ):
        return pd.DataFrame()

    x = df.copy()

    x["date"] = pd.to_datetime(
        x["date"],
        errors="coerce",
    )

    aliases = {
        "外資": [
            "Foreign_Investor",
            "Foreign_Investor_buy_sell",
            "foreign_investor",
        ],
        "投信": [
            "Investment_Trust",
            "Investment_Trust_buy_sell",
            "investment_trust",
        ],
        "自營商": [
            "Dealer_Self",
            "Dealer_Self_buy_sell",
            "Dealer",
        ],
    }

    dates = sorted(
        x["date"]
        .dropna()
        .unique()
    )

    result = pd.DataFrame(
        {
            "date": dates
        }
    )

    for name, candidates in aliases.items():
        found = next(
            (
                c
                for c in candidates
                if c in x.columns
            ),
            None,
        )

        if found:
            temp = pd.to_numeric(
                x[found],
                errors="coerce",
            ).fillna(0)

            grouped = (
                temp
                .groupby(x["date"])
                .sum()
            )

            result[name] = (
                result["date"]
                .map(grouped)
                .fillna(0)
            )
        else:
            result[name] = 0.0

    return result


# ============================================================
# 市值 Top 500
# ============================================================

@st.cache_data(
    ttl=86400,
    show_spinner=False,
)
def get_market_value_top500():
    try:
        end_date = (
            datetime.now().date()
        )

        start_date = (
            end_date
            - timedelta(days=10)
        )

        response = requests.get(
            FINMIND_API,
            params={
                "dataset":
                    "TaiwanStockMarketValue",
                "start_date":
                    str(start_date),
                "end_date":
                    str(end_date),
            },
            timeout=30,
        )

        response.raise_for_status()

        df = pd.DataFrame(
            response.json().get(
                "data",
                [],
            )
        )

        required = {
            "date",
            "stock_id",
            "market_value",
        }

        if (
            df.empty
            or not required.issubset(
                df.columns
            )
        ):
            return []

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
        )

        latest_date = df["date"].max()

        latest = df[
            df["date"] == latest_date
        ].copy()

        latest["market_value"] = (
            pd.to_numeric(
                latest["market_value"],
                errors="coerce",
            )
        )

        latest = (
            latest
            .dropna(
                subset=["market_value"]
            )
            .sort_values(
                "market_value",
                ascending=False,
            )
            .head(500)
        )

        return [
            normalize_code(x)
            for x in latest[
                "stock_id"
            ].astype(str)
        ]

    except Exception:
        return []


# ============================================================
# 智慧選股
# ============================================================

def scan_one(
    code,
    params,
):
    df = get_history(
        code,
        1.0,
    )

    if (
        df.empty
        or len(df) < 80
    ):
        return None

    box_ok, box_info = (
        detect_box_breakout(
            df,
            box_days=params[
                "box_days"
            ],
            max_width=params[
                "box_width"
            ],
            breakout_max=params[
                "breakout_pct"
            ],
            vol_mult=params[
                "vol_mult"
            ],
        )
    )

    bottom_ok, _ = (
        detect_head_and_shoulders_bottom(
            df,
            order=5,
            right_window=params[
                "right_window"
            ],
            shoulder_diff_limit=params[
                "shoulder_diff"
            ],
            neckline_lower=(
                1
                - params[
                    "neckline_buffer"
                ]
            ),
            neckline_upper=1.08,
        )
    )

    top_ok, _ = (
        detect_head_and_shoulders_top(
            df,
            order=5,
            right_window=params[
                "right_window"
            ],
            shoulder_diff_limit=params[
                "shoulder_diff"
            ],
            neckline_lower=0.85,
            neckline_upper=(
                1
                + params[
                    "neckline_buffer"
                ]
            ),
        )
    )

    signal_count = (
        int(box_ok)
        + int(bottom_ok)
        + int(top_ok)
    )

    if signal_count == 0:
        return None

    result = {
        "股票代號":
            normalize_code(code),
        "股票名稱":
            get_stock_name(code),
        "最新收盤":
            float(
                df["Close"].iloc[-1]
            ),
        "箱型突破":
            "✅" if box_ok else "",
        "頭肩底":
            "✅" if bottom_ok else "",
        "頭肩頂":
            "⚠️" if top_ok else "",
        "訊號數":
            signal_count,
    }

    if box_ok:
        result["箱型振幅"] = (
            f"{box_info['amplitude'] * 100:.1f}%"
        )

        result["突破量比"] = (
            f"{box_info['volume_ratio']:.1f}x"
        )
    else:
        result["箱型振幅"] = ""
        result["突破量比"] = ""

    return result


def run_scan(
    codes,
    params,
):
    rows = []

    progress = st.progress(0)

    total = len(codes)

    for i, code in enumerate(
        codes,
        1,
    ):
        try:
            result = scan_one(
                code,
                params,
            )

            if result:
                rows.append(result)

        except Exception:
            pass

        progress.progress(
            i / total
        )

    progress.empty()

    return pd.DataFrame(rows)


# ============================================================
# Sidebar
# ============================================================

st.sidebar.title(
    "⚙️ 系統設定"
)

symbol = normalize_code(
    st.sidebar.text_input(
        "台股代號",
        "2330",
        help="例如 2330，不需要輸入 .TW",
    )
)

period_years = (
    st.sidebar.select_slider(
        "觀察期間（年）",
        options=[
            1.0,
            1.5,
            2.0,
            2.5,
            3.0,
            3.5,
            4.0,
            4.5,
            5.0,
        ],
        value=3.5,
    )
)

st.sidebar.markdown("---")

st.sidebar.subheader(
    "⭐ 常用個股管理"
)

if "favorites" not in st.session_state:
    st.session_state.favorites = (
        COMMON_STOCKS.copy()
    )

favorite = st.sidebar.selectbox(
    "快速選擇",
    ["（目前輸入）"]
    + st.session_state.favorites,
)

if favorite != "（目前輸入）":
    symbol = favorite

st.sidebar.caption(
    f"共 {len(st.session_state.favorites)} 檔"
)

current_name = get_stock_name(
    symbol
)

display_name = (
    f"{symbol} {current_name}"
).strip()

# ============================================================
# Header
# ============================================================

st.title(
    "📈 樂活五線譜與智慧選股系統"
)

st.caption(
    f"目前分析：{display_name}"
    "　｜　幣別：新台幣 NT$"
)

tab_lohas, tab_kline, tab_scan = (
    st.tabs(
        [
            "📊 樂活五線譜",
            "📈 K線與指標",
            "🔍 智慧型態選股",
        ]
    )
)

# ============================================================
# Tab 1：樂活五線譜
# ============================================================

with tab_lohas:

    st.subheader(
        f"📊 {display_name}｜樂活五線譜"
    )

    df = get_history(
        symbol,
        period_years,
    )

    if df.empty:

        st.error(
            "無法取得此股票資料，"
            "請確認代號是否正確或稍後再試。"
        )

    else:

        close = float(
            df["Close"].iloc[-1]
        )

        prev = float(
            df["Close"].iloc[-2]
        )

        change = (
            close - prev
        )

        pct = (
            change / prev * 100
            if prev
            else 0
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "最新收盤",
            f"NT$ {close:,.2f}",
            f"{change:+.2f}",
        )

        c2.metric(
            "漲跌幅",
            f"{pct:+.2f}%",
        )

        c3.metric(
            "觀察期間",
            f"{period_years:.1f} 年",
        )

        lohas = calculate_lohas(
            df,
            period_years,
        )

        if lohas.empty:

            st.warning(
                "資料不足，"
                "無法建立樂活五線譜。"
            )

        else:

            fig = go.Figure()

            line_specs = [
                (
                    "極度貪婪",
                    "#8E245E",
                ),
                (
                    "貪婪",
                    "#C44E52",
                ),
                (
                    "趨勢線",
                    "#777777",
                ),
                (
                    "恐懼",
                    "#4F81BD",
                ),
                (
                    "極度恐懼",
                    "#2F5597",
                ),
                (
                    "股價",
                    "#222222",
                ),
            ]

            for label, color in line_specs:

                width = (
                    2
                    if label == "趨勢線"
                    else 1.5
                )

                fig.add_trace(
                    go.Scatter(
                        x=lohas.index,
                        y=lohas[label],
                        mode="lines",
                        name=label,
                        line=dict(
                            color=color,
                            width=width,
                        ),
                        hovertemplate=(
                            f"日期：%{{x|%Y-%m-%d}}"
                            f"<br>{label}："
                            "NT$ %{y:.2f}"
                            "<extra></extra>"
                        ),
                    )
                )

            fig.update_layout(
                template="plotly_white",
                paper_bgcolor="white",
                plot_bgcolor="white",
                height=560,
                hovermode="x unified",
                margin=dict(
                    l=10,
                    r=10,
                    t=25,
                    b=30,
                ),
                legend=dict(
                    orientation="h",
                    y=1.02,
                    x=0,
                ),
                xaxis=dict(
                    side="bottom",
                    showgrid=True,
                ),
                yaxis=dict(
                    title="NT$",
                    side="right",
                    showgrid=True,
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

            st.info(
                "越靠近極度貪婪代表估值偏高；"
                "越靠近極度恐懼代表估值偏低。"
                "五線譜僅供估值與趨勢輔助判讀。"
            )


# ============================================================
# Tab 2：K線與指標
# ============================================================

with tab_kline:

    st.subheader(
        f"📈 {display_name}｜K線與技術指標"
    )

    df = get_history(
        symbol,
        period_years,
    )

    if df.empty:

        st.error(
            "無法取得股票資料。"
        )

    else:

        ind = add_indicators(df)

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.04,
            row_heights=[
                0.72,
                0.28,
            ],
        )

        fig.add_trace(
            go.Candlestick(
                x=ind.index,
                open=ind["Open"],
                high=ind["High"],
                low=ind["Low"],
                close=ind["Close"],
                name="K線",
            ),
            row=1,
            col=1,
        )

        ma_specs = [
            ("MA5", "#8E44AD"),
            ("MA20", "#E67E22"),
            ("MA60", "#27AE60"),
            ("MA120", "#2980B9"),
            ("MA240", "#7F8C8D"),
        ]

        for ma, color in ma_specs:

            fig.add_trace(
                go.Scatter(
                    x=ind.index,
                    y=ind[ma],
                    mode="lines",
                    name=ma,
                    line=dict(
                        color=color,
                        width=1.2,
                    ),
                ),
                row=1,
                col=1,
            )

        fig.add_trace(
            go.Bar(
                x=ind.index,
                y=ind["Volume"],
                name="成交量",
            ),
            row=2,
            col=1,
        )

        fig.update_layout(
            template="plotly_white",
            height=650,
            xaxis_rangeslider_visible=False,
            hovermode="x unified",
            margin=dict(
                l=5,
                r=5,
                t=25,
                b=20,
            ),
            legend=dict(
                orientation="h",
                y=1.02,
                x=0,
            ),
        )

        fig.update_yaxes(
            side="right"
        )

        fig.update_xaxes(
            side="bottom"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
            },
        )

        indicator = st.radio(
            "下方指標",
            [
                "成交量",
                "KD 指標",
                "MACD",
                "RSI",
                "主力 vs 散戶",
                "三大法人",
            ],
            horizontal=True,
        )

        # ----------------------------------------------------
        # 成交量
        # ----------------------------------------------------

        if indicator == "成交量":

            f = go.Figure()

            f.add_trace(
                go.Bar(
                    x=ind.index,
                    y=ind["Volume"],
                    name="成交量",
                )
            )

            f.update_layout(
                template="plotly_white",
                height=300,
                hovermode="x unified",
                yaxis=dict(
                    side="right"
                ),
                xaxis=dict(
                    side="bottom"
                ),
            )

            st.plotly_chart(
                f,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ----------------------------------------------------
        # KD
        # ----------------------------------------------------

        elif indicator == "KD 指標":

            f = go.Figure()

            f.add_trace(
                go.Scatter(
                    x=ind.index,
                    y=ind["K"],
                    mode="lines",
                    name="K",
                )
            )

            f.add_trace(
                go.Scatter(
                    x=ind.index,
                    y=ind["D"],
                    mode="lines",
                    name="D",
                )
            )

            f.add_hline(
                y=80,
                line_dash="dot",
            )

            f.add_hline(
                y=20,
                line_dash="dot",
            )

            f.update_layout(
                template="plotly_white",
                height=320,
                title="KD 指標",
                hovermode="x unified",
                yaxis=dict(
                    side="right",
                    range=[
                        0,
                        100,
                    ],
                ),
                xaxis=dict(
                    side="bottom"
                ),
            )

            st.plotly_chart(
                f,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ----------------------------------------------------
        # MACD
        # ----------------------------------------------------

        elif indicator == "MACD":

            f = go.Figure()

            f.add_trace(
                go.Bar(
                    x=ind.index,
                    y=ind[
                        "MACD_HIST"
                    ],
                    name="柱狀體",
                )
            )

            f.add_trace(
                go.Scatter(
                    x=ind.index,
                    y=ind["DIF"],
                    mode="lines",
                    name="DIF",
                )
            )

            f.add_trace(
                go.Scatter(
                    x=ind.index,
                    y=ind["MACD"],
                    mode="lines",
                    name="MACD",
                )
            )

            f.update_layout(
                template="plotly_white",
                height=320,
                title="MACD",
                hovermode="x unified",
                yaxis=dict(
                    side="right"
                ),
                xaxis=dict(
                    side="bottom"
                ),
            )

            st.plotly_chart(
                f,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ----------------------------------------------------
        # RSI
        # ----------------------------------------------------

        elif indicator == "RSI":

            f = go.Figure()

            f.add_trace(
                go.Scatter(
                    x=ind.index,
                    y=ind["RSI"],
                    mode="lines",
                    name="RSI",
                )
            )

            f.add_hline(
                y=70,
                line_dash="dot",
            )

            f.add_hline(
                y=30,
                line_dash="dot",
            )

            f.update_layout(
                template="plotly_white",
                height=320,
                title="RSI",
                hovermode="x unified",
                yaxis=dict(
                    side="right",
                    range=[
                        0,
                        100,
                    ],
                ),
                xaxis=dict(
                    side="bottom"
                ),
            )

            st.plotly_chart(
                f,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ----------------------------------------------------
        # 主力 vs 散戶
        # ----------------------------------------------------

        elif indicator == "主力 vs 散戶":

            st.markdown(
                "### 🏦 主力買賣超 vs 散戶買賣超"
            )

            token = st.text_input(
                "FinMind API Token（此資料需具備對應權限）",
                type="password",
                key="chip_token",
            )

            end_date = (
                datetime.now().date()
            )

            start_date = (
                end_date
                - timedelta(days=90)
            )

            branch = get_branch_agg(
                symbol,
                str(start_date),
                str(end_date),
                token,
            )

            chip = calculate_main_retail(
                branch
            )

            if chip.empty:

                st.warning(
                    "目前沒有取得分點資料。"
                    "請輸入具備對應權限的 FinMind Token。"
                )

            else:

                f = make_subplots(
                    rows=2,
                    cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.08,
                    row_heights=[
                        0.55,
                        0.45,
                    ],
                )

                f.add_trace(
                    go.Bar(
                        x=chip["date"],
                        y=chip["Main"],
                        name="主力買賣超",
                    ),
                    row=1,
                    col=1,
                )

                f.add_trace(
                    go.Bar(
                        x=chip["date"],
                        y=chip["Retail"],
                        name="散戶買賣超（估計）",
                    ),
                    row=1,
                    col=1,
                )

                f.add_trace(
                    go.Scatter(
                        x=chip["date"],
                        y=chip["MainCum"],
                        mode="lines",
                        name="主力累計",
                    ),
                    row=2,
                    col=1,
                )

                f.add_trace(
                    go.Scatter(
                        x=chip["date"],
                        y=chip["RetailCum"],
                        mode="lines",
                        name="散戶累計",
                    ),
                    row=2,
                    col=1,
                )

                f.add_hline(
                    y=0,
                    line_dash="dot",
                    row=1,
                    col=1,
                )

                f.update_layout(
                    template="plotly_white",
                    height=560,
                    hovermode="x unified",
                    barmode="relative",
                    margin=dict(
                        l=5,
                        r=5,
                        t=25,
                        b=20,
                    ),
                )

                f.update_yaxes(
                    side="right"
                )

                f.update_xaxes(
                    side="bottom"
                )

                st.plotly_chart(
                    f,
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                    },
                )

                st.caption(
                    "主力／散戶是分點交易結構推估；"
                    "散戶並非直接觀察個別自然人帳戶，"
                    "因此僅作參考。"
                )

        # ----------------------------------------------------
        # 三大法人
        # ----------------------------------------------------

        else:

            inst = get_institutional(
                symbol,
                str(
                    datetime.now().date()
                    - timedelta(days=90)
                ),
                str(
                    datetime.now().date()
                ),
            )

            inst = prepare_institutional(
                inst
            )

            if inst.empty:

                st.warning(
                    "目前無法取得三大法人資料。"
                )

            else:

                f = go.Figure()

                for col in [
                    "外資",
                    "投信",
                    "自營商",
                ]:

                    f.add_trace(
                        go.Bar(
                            x=inst["date"],
                            y=inst[col],
                            name=col,
                        )
                    )

                f.update_layout(
                    template="plotly_white",
                    height=360,
                    barmode="relative",
                    hovermode="x unified",
                    yaxis=dict(
                        side="right"
                    ),
                    xaxis=dict(
                        side="bottom"
                    ),
                )

                st.plotly_chart(
                    f,
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                    },
                )


# ============================================================
# Tab 3：智慧型態選股
# ============================================================

with tab_scan:

    st.subheader(
        "🔍 智慧型態選股"
    )

    st.info(
        "四級條件已重新配置；"
        "「嚴格」就是你這次提供的新版條件："
        "60 日箱型、20% 最大振幅、突破 0～5%、"
        "成交量 1.3 倍，以及頭肩型態最近 20 日、"
        "左右肩差異 <10%。"
    )

    # --------------------------------------------------------
    # 選股範圍
    # --------------------------------------------------------

    universe = st.radio(
        "選股範圍",
        [
            "常用個股",
            "市值 Top 500",
            "自訂清單",
        ],
        horizontal=True,
    )

    if universe == "常用個股":

        codes = COMMON_STOCKS

    elif universe == "市值 Top 500":

        codes = (
            get_market_value_top500()
        )

        if not codes:

            st.warning(
                "目前無法取得市值 Top 500；"
                "請改用常用個股或自訂清單。"
            )

    else:

        custom = st.text_area(
            "自訂股票代號",
            "2330,2454,2308,2317",
            help=(
                "可用逗號、空白或換行分隔，"
                "不需要 .TW"
            ),
        )

        codes = [
            normalize_code(x)
            for x in custom
            .replace(",", " ")
            .replace("，", " ")
            .split()
            if normalize_code(x)
        ]

    # --------------------------------------------------------
    # 四級嚴格程度
    # --------------------------------------------------------

    strength = st.radio(
        "篩選嚴格程度",
        [
            "寬鬆",
            "標準",
            "嚴格",
            "極嚴格",
        ],
        index=2,
        horizontal=True,
    )

    preset = PRESETS[strength]

    st.markdown(
        "### 🔧 進階參數"
    )

    # 使用不同 key 綁定四級，
    # 切換級別時會真正載入該級預設值。
    box_days = st.slider(
        "箱型整理天數",
        20,
        100,
        int(
            preset["box_days"]
        ),
        5,
        key=f"box_days_{strength}",
    )

    box_width_pct = st.slider(
        "箱型最大振幅 (%)",
        5.0,
        35.0,
        preset["box_width"] * 100,
        0.5,
        key=f"box_width_{strength}",
    )

    breakout_pct = st.slider(
        "突破後最大漲幅 (%)",
        1.0,
        10.0,
        preset["breakout_pct"] * 100,
        0.5,
        key=f"breakout_{strength}",
    )

    vol_mult = st.slider(
        "突破成交量 / 20日均量",
        1.0,
        2.5,
        preset["vol_mult"],
        0.1,
        key=f"vol_{strength}",
    )

    shoulder_diff_pct = st.slider(
        "頭肩左右肩最大差異 (%)",
        3.0,
        20.0,
        preset["shoulder_diff"] * 100,
        0.5,
        key=f"shoulder_{strength}",
    )

    right_window = st.slider(
        "右肩／右底距今最多天數",
        10,
        45,
        int(
            preset["right_window"]
        ),
        1,
        key=f"right_{strength}",
    )

    neckline_buffer_pct = st.slider(
        "頸線附近允許幅度 (%)",
        1.0,
        10.0,
        preset["neckline_buffer"] * 100,
        0.5,
        key=f"neckline_{strength}",
    )

    params = {
        "box_days":
            box_days,
        "box_width":
            box_width_pct / 100,
        "breakout_pct":
            breakout_pct / 100,
        "vol_mult":
            vol_mult,
        "shoulder_diff":
            shoulder_diff_pct / 100,
        "right_window":
            right_window,
        "neckline_buffer":
            neckline_buffer_pct / 100,
    }

    # --------------------------------------------------------
    # 實際參數表
    # --------------------------------------------------------

    with st.expander(
        "📋 目前實際篩選參數",
        expanded=False,
    ):

        parameter_df = pd.DataFrame(
            {
                "參數": [
                    "箱型整理天數",
                    "箱型最大振幅",
                    "突破後最大漲幅",
                    "突破量能倍數",
                    "左右肩最大差異",
                    "右肩／右底距今最多天數",
                    "頸線附近允許幅度",
                ],
                "目前值": [
                    f"{box_days} 日",
                    f"{box_width_pct:.1f}%",
                    f"{breakout_pct:.1f}%",
                    f"{vol_mult:.1f} 倍",
                    f"{shoulder_diff_pct:.1f}%",
                    f"{right_window} 日",
                    f"{neckline_buffer_pct:.1f}%",
                ],
            }
        )

        st.dataframe(
            parameter_df,
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        f"目前預設：{strength}。"
        "「嚴格」已直接採用本次新版條件。"
    )

    # --------------------------------------------------------
    # 開始掃描
    # --------------------------------------------------------

    if st.button(
        "🚀 開始智慧型態掃描",
        type="primary",
        use_container_width=True,
    ):

        if not codes:

            st.warning(
                "沒有可掃描的股票。"
            )

        else:

            st.write(
                f"正在掃描 {len(codes)} 檔股票……"
            )

            result = run_scan(
                codes,
                params,
            )

            if result.empty:

                st.warning(
                    "目前沒有符合條件的股票；"
                    "可切換「標準」或「寬鬆」擴大範圍。"
                )

            else:

                result = (
                    result
                    .sort_values(
                        [
                            "訊號數",
                            "股票代號",
                        ],
                        ascending=[
                            False,
                            True,
                        ],
                    )
                    .reset_index(
                        drop=True
                    )
                )

                st.success(
                    f"掃描完成，共找到 "
                    f"{len(result)} 檔符合至少一項型態。"
                )

                result["股票"] = (
                    result["股票代號"]
                    + " "
                    + result["股票名稱"]
                ).str.strip()

                display_columns = [
                    "股票",
                    "最新收盤",
                    "箱型突破",
                    "頭肩底",
                    "頭肩頂",
                    "訊號數",
                    "箱型振幅",
                    "突破量比",
                ]

                st.dataframe(
                    result[
                        display_columns
                    ],
                    use_container_width=True,
                    hide_index=True,
                )

                st.caption(
                    "型態訊號僅為技術分析輔助，"
                    "不代表必然上漲或下跌；"
                    "建議搭配成交量、均線、法人"
                    "與大盤環境判斷。"
                )


# ============================================================
# Footer
# ============================================================

st.markdown("---")

st.caption(
    "資料主要來自 Yahoo Finance；"
    "股票名稱與部分籌碼資料使用 FinMind。"
    "資料可能因來源、權限、更新時間或網路狀況有所延遲。"
)