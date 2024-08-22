import random

# Danh sách điểm khởi đầu và điểm đích
all_init_points = [41, 43, 44, 46, 47, 49, 50, 52, 53, 55, 56, 58, 101, 103, 104, 106, 107, 109, 110, 112, 113, 115, 116, 118, 161, 163, 164, 166, 167, 169, 170, 172, 173, 175, 176, 178, 221, 223, 224, 226, 227, 229, 230, 232, 233, 235, 236, 238, 281, 283, 284, 286, 287, 289, 290, 292, 293, 295, 296, 298, 341, 343, 344, 346, 347, 349, 350, 352, 353, 355, 356, 358]
all_target_points = [358, 356, 355, 353, 352, 350, 349, 347, 346, 344, 343, 341, 298, 296, 295, 293, 292, 290, 289, 287, 286, 284, 283, 281, 238, 236, 235, 233, 232, 230, 229, 227, 226, 224, 223, 221, 178, 176, 175, 173, 172, 170, 169, 167, 166, 164, 163, 161, 118, 116, 115, 113, 112, 110, 109, 107, 106, 104, 103, 101, 58, 56, 55, 53, 52, 50, 49, 47, 46, 44, 43, 41]

# Đảm bảo danh sách các chỉ số
indices = list(range(len(all_init_points)))
random.shuffle(indices)

# Tạo danh sách test
test_init_points = []
test_target_points = []

count = 0
for index in indices:
    if count >= 28:
        break
    if all_init_points[index] != all_target_points[index]:
        test_init_points.append(all_init_points[index])
        test_target_points.append(all_target_points[index])
        count += 1

# Kết quả
print("Test init points:", test_init_points)
print("Test target points:", test_target_points)