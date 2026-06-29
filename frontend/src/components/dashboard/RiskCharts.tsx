"use client";
import ReactECharts from "echarts-for-react";

export function RiskDistributionChart() {
  const options = {
    title: { text: "Distribusi Kategori Risiko", left: "center" },
    tooltip: { trigger: "item" },
    legend: { bottom: "0%" },
    series: [
      {
        name: "Risiko",
        type: "pie",
        radius: ["40%", "70%"],
        data: [
          { value: 1048, name: "Tinggi", itemStyle: { color: "#F28A6A" } },
          { value: 735, name: "Sedang", itemStyle: { color: "#FF7A3D" } },
          { value: 580, name: "Rendah", itemStyle: { color: "#52C7D8" } },
        ]
      }
    ]
  };
  return <ReactECharts option={options} style={{ height: "100%", width: "100%" }} />;
}

export function BudgetTrendChart() {
  const options = {
    title: { text: "Tren Pagu vs Prediksi Wajar P90", left: "center" },
    tooltip: { trigger: "axis" },
    xAxis: { type: "category", data: ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun"] },
    yAxis: { type: "value" },
    series: [
      { data: [820, 932, 901, 934, 1290, 1330], type: "line", name: "Pagu Asli", smooth: true, itemStyle: { color: "#0D5CBD" } },
      { data: [800, 900, 850, 900, 1100, 1200], type: "line", name: "P90 (Wajar)", smooth: true, itemStyle: { color: "#8A63E8" }, lineStyle: { type: "dashed" } },
    ]
  };
  return <ReactECharts option={options} style={{ height: "100%", width: "100%" }} />;
}
