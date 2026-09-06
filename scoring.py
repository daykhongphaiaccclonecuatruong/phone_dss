def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(value, maximum))


def scale(value, low, high):
    """
    Chuẩn hóa một giá trị về thang 0-100.
    """
    if high == low:
        return 0

    score = (value - low) / (high - low) * 100
    return clamp(score)


def panel_score(display_type):
    display_type = str(display_type).lower()

    if "dynamic amoled" in display_type:
        return 100

    if "super amoled" in display_type:
        return 98

    if "amoled" in display_type:
        return 95

    if "oled" in display_type:
        return 95

    if "ips" in display_type:
        return 70

    return 50


def calculate_camera_score(row):
    mp_score = scale(row["main_camera_mp"], 12, 200)

    ois_score = 100 if row["ois"] == 1 else 0

    zoom_score = scale(row["optical_zoom_x"], 0, 5)

    # Khẩu độ càng nhỏ càng tốt
    aperture_score = scale(
        2.5 - row["main_camera_aperture"],
        0,
        1.1
    )

    score = (
        mp_score * 0.30
        + ois_score * 0.30
        + zoom_score * 0.25
        + aperture_score * 0.15
    )

    return round(clamp(score), 2)


def calculate_gaming_score(row):
    benchmark_score = scale(
        row["antutu_score"],
        300000,
        2500000
    )

    ram_score = scale(
        row["ram_gb"],
        4,
        16
    )

    refresh_score = scale(
        row["refresh_rate_hz"],
        60,
        144
    )

    screen_score = panel_score(row["display_type"])

    score = (
        benchmark_score * 0.55
        + ram_score * 0.20
        + refresh_score * 0.15
        + screen_score * 0.10
    )

    return round(clamp(score), 2)


def calculate_battery_score(row):
    capacity_score = scale(
        row["battery_mah"],
        3000,
        6000
    )

    charging_score = scale(
        row["charging_w"],
        15,
        120
    )

    score = (
        capacity_score * 0.65
        + charging_score * 0.35
    )

    return round(clamp(score), 2)


def calculate_display_score(row):
    refresh_score = scale(
        row["refresh_rate_hz"],
        60,
        144
    )

    pixels = (
        row["resolution_width"]
        * row["resolution_height"]
    )

    resolution_score = scale(
        pixels,
        2000000,
        4600000
    )

    screen_score = panel_score(row["display_type"])

    score = (
        refresh_score * 0.35
        + resolution_score * 0.35
        + screen_score * 0.30
    )

    return round(clamp(score), 2)


def calculate_thin_light_score(row):
    # Càng nhẹ càng tốt
    weight_score = scale(
        230 - row["weight_g"],
        0,
        80
    )

    # Càng mỏng càng tốt
    thickness_score = scale(
        10 - row["thickness_mm"],
        0,
        3.5
    )

    score = (
        weight_score * 0.60
        + thickness_score * 0.40
    )

    return round(clamp(score), 2)


def calculate_all_scores(row):
    return {
        "camera_score": calculate_camera_score(row),
        "gaming_score": calculate_gaming_score(row),
        "battery_score": calculate_battery_score(row),
        "display_score": calculate_display_score(row),
        "thin_light_score": calculate_thin_light_score(row)
    }