import sys

from recommender import recommend


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")


print("=" * 50)
print("HỆ TRỢ GIÚP QUYẾT ĐỊNH CHỌN ĐIỆN THOẠI")
print("=" * 50)

min_budget = float(
    input(
        "Ngân sách tối thiểu (triệu đồng): "
    )
)

max_budget = float(
    input(
        "Ngân sách tối đa (triệu đồng): "
    )
)

print("\nTình trạng máy:")
print("1. Máy mới")
print("2. Máy cũ")

condition_choice = input(
    "Chọn 1 hoặc 2: "
)

if condition_choice == "2":
    condition = "used"
else:
    condition = "new"


print("\nCác tiêu chí:")
print("1. Camera")
print("2. Gaming")
print("3. Pin")
print("4. Màn hình")
print("5. Mỏng nhẹ")

priority_mapping = {
    "1": "camera",
    "2": "gaming",
    "3": "battery",
    "4": "display",
    "5": "thin_light"
}

priority_1 = input(
    "Tiêu chí ưu tiên số 1: "
)

priority_1 = priority_mapping.get(
    priority_1,
    "camera"
)

use_second = input(
    "Có tiêu chí ưu tiên thứ 2 không? (y/n): "
)

priorities = [priority_1]

if use_second.lower() == "y":
    priority_2 = input(
        "Tiêu chí ưu tiên số 2: "
    )

    priority_2 = priority_mapping.get(
        priority_2
    )

    if (
        priority_2
        and priority_2 != priority_1
    ):
        priorities.append(priority_2)


results = recommend(
    min_budget,
    max_budget,
    condition,
    priorities
)


print("\n" + "=" * 50)
print("KẾT QUẢ GỢI Ý")
print("=" * 50)


if results.empty:
    print(
        "Không tìm thấy điện thoại phù hợp "
        "với ngân sách và yêu cầu của bạn."
    )

else:
    for index, (_, row) in enumerate(
        results.iterrows(),
        start=1
    ):
        print(
            f"\nTOP {index}: "
            f"{row['brand']} "
            f"{row['model_name']}"
        )

        print(
            f"Phiên bản: {row['variant']}"
        )

        print(
            f"Giá: "
            f"{int(row['price']):,} đồng"
        )

        print(
            f"Điểm phù hợp: "
            f"{row['final_score']}/100"
        )

        print(
            f"Camera: "
            f"{row['camera_score']}/100"
        )

        print(
            f"Gaming: "
            f"{row['gaming_score']}/100"
        )

        print(
            f"Pin: "
            f"{row['battery_score']}/100"
        )

        print(
            f"Màn hình: "
            f"{row['display_score']}/100"
        )

        print(
            f"Mỏng nhẹ: "
            f"{row['thin_light_score']}/100"
        )

        print(
            f"Value: "
            f"{row['value_score']:.2f}/100"
        )

        print(
            "Lý do:",
            row["reason"]
        )
