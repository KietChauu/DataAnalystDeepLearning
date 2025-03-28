import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy.stats as stats
import numpy as np

# Đọc dữ liệu từ file CSV
file_path = "processed_dulieuxettuyendaihoc.csv"
df = pd.read_csv(file_path)

# Phần 1:
# Câu 1: Sắp xếp dữ liệu điểm DH1 theo thứ tự tăng dần
df_sorted_dh1 = df.sort_values(by="DH1", ascending=True)
print("Dữ liệu sắp xếp theo DH1 tăng dần:")
print(df_sorted_dh1[["DH1"]])

# Câu 2: Sắp xếp dữ liệu điểm DH2 tăng dần theo nhóm giới tính (GT)
df_sorted_dh2_gt = df.sort_values(by=["GT", "DH2"], ascending=[True, True])
print("\nDữ liệu sắp xếp theo DH2 và GT:")
print(df_sorted_dh2_gt[["GT", "DH2"]])

# Câu 3: Tạo pivot-table thống kê DH1 theo KT
pivot_dh1_kt = df.pivot_table(
    values="DH1",
    index="KT",
    aggfunc=["count", "sum", "mean", "median", "min", "max", "std",
             lambda x: x.quantile(0.25), lambda x: x.quantile(0.50), lambda x: x.quantile(0.75)]
)
print("Tổng điểm DH1:", df["DH1"].sum())
pivot_dh1_kt.columns = ["count", "sum", "mean",
                        "median", "min", "max", "std", "Q1", "Q2", "Q3"]
print("\nPivot-table DH1 theo KT:")
print(pivot_dh1_kt)

# Câu 4: Tạo pivot-table thống kê DH1 theo KT và KV
pivot_dh1_kt_kv = df.pivot_table(
    values="DH1",
    index=["KT", "KV"],
    aggfunc=["count", "sum", "mean", "median", "min", "max", "std",
             lambda x: x.quantile(0.25), lambda x: x.quantile(0.50), lambda x: x.quantile(0.75)]
)
pivot_dh1_kt_kv.columns = ["count", "sum", "mean",
                           "median", "min", "max", "std", "Q1", "Q2", "Q3"]
print("\nPivot-table DH1 theo KT và KV:")
print(pivot_dh1_kt_kv)

# Câu 5: Tạo pivot-table thống kê DH1 theo KT, KV và DT
pivot_dh1_kt_kv_dt = df.pivot_table(
    values="DH1",
    index=["KT", "KV", "DT"],
    aggfunc=["count", "sum", "mean", "median", "min", "max", "std",
             lambda x: x.quantile(0.25), lambda x: x.quantile(0.50), lambda x: x.quantile(0.75)]
)
pivot_dh1_kt_kv_dt.columns = ["count", "sum", "mean",
                              "median", "min", "max", "std", "Q1", "Q2", "Q3"]
print("\nPivot-table DH1 theo KT, KV và DT:")
print(pivot_dh1_kt_kv_dt)

# Phần 2:
# Câu 1: Trình bày dữ liệu biến GT
# Lập bảng tần số và tần suất
gt_counts = df["GT"].value_counts()
gt_frequencies = df["GT"].value_counts(normalize=True) * 100

gt_table = pd.DataFrame({"Tần số": gt_counts, "Tần suất (%)": gt_frequencies})
print("Bảng tần số và tần suất của GT:")
print(gt_table)

# Vẽ biểu đồ tần số (cột)
plt.figure(figsize=(8, 5))
gt_counts.plot(kind="bar", color=["blue", "orange"])
plt.title("Biểu đồ tần số của GT")
plt.xlabel("Giới tính")
plt.ylabel("Tần số")
plt.xticks(rotation=0)
plt.show()

# Vẽ biểu đồ tần suất (tròn)
plt.figure(figsize=(6, 6))
gt_counts.plot(kind="pie", autopct="%.1f%%", colors=[
               "blue", "orange"], startangle=90)
plt.title("Biểu đồ tần suất của GT")
plt.ylabel("")  # Ẩn nhãn trục y
plt.show()

# Câu 2: Trình bày dữ liệu lần lượt các biến US_TBM1, US_TBM2 và US_TBM3
us_tbm_columns = ["US_TBM1", "US_TBM2", "US_TBM3"]
print("\nThống kê mô tả cho US_TBM1, US_TBM2, US_TBM3:")
print(df[us_tbm_columns].describe())

# Câu 3: Trình bày dữ liệu biến DT với các học sinh là nam
dt_nam = df[df["GT"] == "M"]  # Chỉnh GT thành 'M' thay vì 'Nam'
dt_grouped = dt_nam.groupby("DT")["DT"].agg("count")
print("\nTần số của DT cho học sinh nam:")
print(dt_grouped)

# Câu 4: Trình bày dữ liệu biến KV với các học sinh là nam thuộc dân tộc Kinh, có điểm thỏa mãn điều kiện
df_filtered = df[(df["GT"] == "M") & (df["DT"] == 1) & (
    df["DH1"] >= 5.0) & (df["DH2"] >= 4.0) & (df["DH3"] >= 4.0)]
kv_grouped = df_filtered.groupby("KV")["KV"].agg("count")
print("\nTần số của KV với học sinh nam thuộc dân tộc Kinh và đủ điều kiện điểm:")
print(kv_grouped)

# Câu 5: Trình bày dữ liệu lần lượt các biến DH1, DH2, DH3 lớn hơn bằng 5.0 và thuộc khu vực 2NT
df_filtered_dh = df[(df["DH1"] >= 5.0) & (df["DH2"] >= 5.0)
                    & (df["DH3"] >= 5.0) & (df["KV"] == "2NT")]
print("\nDữ liệu học sinh có DH1, DH2, DH3 >= 5.0 và thuộc KV 2NT:")
print(df_filtered_dh[["DH1", "DH2", "DH3", "KV"]])

# Lọc dữ liệu học sinh nữ
df_female = df[df["GT"] == "F"]

# Nhóm dữ liệu theo XL1, XL2, XL3
grouped_xl = df_female.groupby(["XL1", "XL2", "XL3"])["GT"].count().unstack()
print("\nBảng tần số học sinh nữ theo XL1, XL2, XL3:")
print(grouped_xl)

# Phần 3:
# Câu 1: Trực quan dữ liệu học sinh nữ trên các nhóm XL1, XL2, XL3 dạng unstacked
# Lọc dữ liệu học sinh nữ
df_female = df[df["GT"] == "F"]
# Nhóm dữ liệu theo XL1, XL2, XL3
grouped_xl = df_female.groupby(["XL1", "XL2", "XL3"])["GT"].count().unstack()
# Hiển thị bảng dữ liệu
df_female_summary = grouped_xl
print("\nBảng tần số học sinh nữ theo XL1, XL2, XL3:")
print(df_female_summary)
# Vẽ biểu đồ cột unstacked để hiển thị số lượng học sinh theo xếp loại
plt.figure(figsize=(10, 6))
df_female_summary.plot(kind="bar", stacked=False, colormap="viridis")
plt.title("Phân bố học sinh nữ theo nhóm XL1, XL2, XL3")
plt.xlabel("Nhóm XL1 và XL2")
plt.ylabel("Số lượng học sinh")
plt.legend(title="Xếp loại XL3")
plt.xticks(rotation=0)
plt.show()


# Câu 2: Trực quan dữ liệu KQXT trên nhóm học sinh có khối thi A, A1, B thuộc khu vực 1, 2
df_kqxt = df[(df["KT"].isin(["A", "A1", "B"])) & (df["KV"].isin(["1", "2"]))]
kqxt_grouped = df_kqxt.groupby(["KT", "KV"])["KQXT"].value_counts().unstack()

# Hiển thị bảng dữ liệu
print("\nBảng KQXT trên nhóm học sinh có khối thi A, A1, B thuộc khu vực 1, 2:")
print(kqxt_grouped)

# Vẽ biểu đồ cột
kqxt_grouped.plot(kind="bar", stacked=True,
                  figsize=(10, 6), colormap="coolwarm")
plt.title("Kết quả xét tuyển theo khối thi và khu vực")
plt.xlabel("Khối thi - Khu vực")
plt.ylabel("Số lượng học sinh")
plt.legend(title="KQXT")
plt.xticks(rotation=45)
plt.show()

# Câu 3: Trực quan dữ liệu số lượng thí sinh từng khu vực dựa trên từng nhóm khối thi
df_khuvuc = df.groupby(["KV", "KT"]).size().unstack()
print("\nBảng số lượng thí sinh theo khu vực và khối thi:")
print(df_khuvuc)

df_khuvuc.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="coolwarm")
plt.title("Số lượng thí sinh theo khu vực và khối thi")
plt.xlabel("Khu vực")
plt.ylabel("Số lượng thí sinh")
plt.legend(title="Khối thi")
plt.xticks(rotation=0)
plt.show()

# Câu 4: Trực quan dữ liệu số lượng thí sinh đậu, rớt trên từng nhóm khối thi
df_kq_kt = df.groupby(["KT", "KQXT"]).size().unstack()
print("\nBảng số lượng thí sinh đậu, rớt theo từng nhóm khối thi:")
print(df_kq_kt)

df_kq_kt.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="coolwarm")
plt.title("Số lượng thí sinh đậu, rớt theo khối thi")
plt.xlabel("Khối thi")
plt.ylabel("Số lượng thí sinh")
plt.legend(title="Kết quả")
plt.xticks(rotation=0)
plt.show()

# Câu 5: Trực quan dữ liệu số lượng thí sinh đậu rớt trên từng nhóm khu vực
df_kq_kv = df.groupby(["KV", "KQXT"]).size().unstack()
print("\nBảng số lượng thí sinh đậu, rớt theo khu vực:")
print(df_kq_kv)

df_kq_kv.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="coolwarm")
plt.title("Số lượng thí sinh đậu, rớt theo khu vực")
plt.xlabel("Khu vực")
plt.ylabel("Số lượng thí sinh")
plt.legend(title="Kết quả")
plt.xticks(rotation=0)
plt.show()

# Câu 6: Trực quan dữ liệu số lượng thí sinh đậu rớt dựa trên từng nhóm dân tộc
df_kq_dt = df.groupby(["DT", "KQXT"]).size().unstack()
print("\nBảng số lượng thí sinh đậu, rớt theo dân tộc:")
print(df_kq_dt)

df_kq_dt.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="coolwarm")
plt.title("Số lượng thí sinh đậu, rớt theo dân tộc")
plt.xlabel("Dân tộc")
plt.ylabel("Số lượng thí sinh")
plt.legend(title="Kết quả")
plt.xticks(rotation=0)
plt.show()

# Câu 7: Trực quan dữ liệu số lượng thí sinh đậu rớt dựa trên từng nhóm giới tính
df_kq_gt = df.groupby(["GT", "KQXT"]).size().unstack()
print("\nBảng số lượng thí sinh đậu, rớt theo giới tính:")
print(df_kq_gt)

df_kq_gt.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="coolwarm")
plt.title("Số lượng thí sinh đậu, rớt theo giới tính")
plt.xlabel("Giới tính")
plt.ylabel("Số lượng thí sinh")
plt.legend(title="Kết quả")
plt.xticks(rotation=0)
plt.show()

# Phần 4 - Trực quan hóa dữ liệu nâng cao
# Câu 1: Vẽ biểu đồ đường Simple cho biến T1
plt.figure(figsize=(10, 6))
t1_counts = df["T1"].value_counts().sort_index()
plt.plot(t1_counts.index, t1_counts.values,
         marker="o", linestyle="-", color="black")
plt.title("Biểu đồ đường Simple cho biến T1")
plt.xlabel("T1")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.grid()
plt.show()

# Câu 2: Tạo biến phân loại (phanlopt1) cho môn toán (T1)


def classify_t1(score):
    if score < 5:
        return "k"
    elif 5 <= score < 7:
        return "tb"
    elif 7 <= score < 8:
        return "kha"
    else:
        return "g"


df["phanlopt1"] = df["T1"].apply(classify_t1)
print("\nDữ liệu sau khi phân loại biến T1:")
print(df[["T1", "phanlopt1"]].head())


# Câu 3: Lập bảng tần số cho biến phanloait1
phanlopt1_counts = df["phanlopt1"].value_counts()
phanlopt1_frequencies = df["phanlopt1"].value_counts(normalize=True) * 100

phanlopt1_table = pd.DataFrame(
    {"Tần số": phanlopt1_counts, "Tần suất (%)": phanlopt1_frequencies})
print("\nBảng tần số và tần suất của phanlopt1:")
print(phanlopt1_table)

# Câu 4: Vẽ biểu đồ đường Multiple Line cho biến T1 được phân loại bởi biến phanlopt1
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x="T1", y=df["T1"].map(
    df["T1"].value_counts()), hue="phanlopt1", palette="coolwarm")
plt.title("Biểu đồ Multiple Line cho biến T1 được phân loại bởi phanlopt1")
plt.xlabel("T1")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.grid()
plt.legend(title="Phân loại T1")
plt.show()

# Câu 5: Vẽ biểu đồ Drop-line cho biến T1 được phân loại bởi biến phanlopt1
plt.figure(figsize=(10, 6))
for category in df["phanlopt1"].unique():
    subset = df[df["phanlopt1"] == category]
    plt.vlines(subset["T1"], ymin=0, ymax=subset["T1"].map(df["T1"].value_counts(
    )), colors=sns.color_palette("coolwarm", len(df["phanlopt1"].unique())), alpha=0.7)
    plt.scatter(subset["T1"], subset["T1"].map(
        df["T1"].value_counts()), label=category, edgecolors="black")

plt.title("Biểu đồ Drop-line cho biến T1 được phân loại bởi phanlopt1")
plt.xlabel("T1")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.grid()
plt.legend(title="Phân loại T1")
plt.show()

# Phần 5 - Mô tả dữ liệu và khảo sát dạng phân phối
# Câu 1: Mô tả và khảo sát phân phối cho biến T1
print("\nMô tả thống kê của biến T1:")
print(df["T1"].describe())

# Vẽ biểu đồ Box-Plot
plt.figure(figsize=(8, 5))
sns.boxplot(x=df["T1"], color="lightblue")
plt.title("Box-Plot của biến T1")
plt.xlabel("T1")
plt.show()

# Vẽ biểu đồ Histogram
plt.figure(figsize=(8, 5))
sns.histplot(df["T1"], bins=20, kde=True, color="lightcoral")
plt.title("Histogram của biến T1")
plt.xlabel("T1")
plt.ylabel("Tần số")
plt.show()

# Vẽ biểu đồ QQ-Plot
plt.figure(figsize=(8, 5))
stats.probplot(df["T1"], dist="norm", plot=plt)
plt.title("QQ-Plot của biến T1")
plt.show()

# Câu 2: Mô tả và khảo sát phân phối của T1 trên từng nhóm phanlopT1
plt.figure(figsize=(8, 5))
sns.boxplot(x=df["phanlopt1"], y=df["T1"],
            hue=df["phanlopt1"], palette="coolwarm")
plt.title("Box-Plot của T1 theo nhóm phanlopT1")
plt.xlabel("phanlopt1")
plt.ylabel("T1")
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="T1", hue="phanlopt1", kde=True,
             multiple="stack", bins=20, palette="coolwarm")
plt.title("Histogram của T1 theo nhóm phanlopT1")
plt.xlabel("T1")
plt.ylabel("Tần số")
plt.show()

# Câu 3: Khảo sát tương quan giữa DH1 theo biến T1
correlation = df[["DH1", "T1"]].corr()
print("\nMa trận tương quan giữa DH1 và T1:")
print(correlation)

plt.figure(figsize=(8, 5))
sns.scatterplot(x=df["T1"], y=df["DH1"],
                hue=df["phanlopt1"], palette="coolwarm", alpha=0.7)
plt.title("Biểu đồ Scatter giữa DH1 và T1")
plt.xlabel("T1")
plt.ylabel("DH1")
plt.show()

# Câu 4: Khảo sát tương quan giữa DH1 theo biến T1 trên từng nhóm khu vực
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="T1", y="DH1", hue="KV",
                palette="coolwarm", alpha=0.7)
plt.title("Biểu đồ Scatter giữa DH1 và T1 theo nhóm khu vực")
plt.xlabel("T1")
plt.ylabel("DH1")
plt.legend(title="Khu vực")
plt.show()

# Câu 5: Khảo sát tương quan giữa DH1, DH2, DH3
correlation_matrix = df[["DH1", "DH2", "DH3"]].corr()
print("\nMa trận tương quan giữa DH1, DH2, DH3:")
print(correlation_matrix)

plt.figure(figsize=(8, 5))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Ma trận tương quan giữa DH1, DH2, DH3")
plt.show()

sns.pairplot(df, vars=["DH1", "DH2", "DH3"],
             hue="phanlopt1", palette="coolwarm")
plt.show()
