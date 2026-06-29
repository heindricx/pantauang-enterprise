"use client";
import ReactECharts from "echarts-for-react";

export function RiskDistributionChart({ data }: { data: any[] }) {
  const options = {
    title: { text: "Distribusi Kategori Risiko", left: "center" },
    tooltip: { trigger: "item" },
    legend: { bottom: "0%" },
    series: [
      {
        name: "Risiko",
        type: "pie",
        radius: ["40%", "70%"],
        data: data || []
      }
    ]
  };
  return <ReactECharts option={options} style={{ height: "100%", width: "100%" }} />;
}

export function BudgetTrendChart({ data }: { data: { months: string[], pagu: number[], p90: number[] } }) {
  const options = {
    title: { text: "Tren Pagu vs Prediksi Wajar P90", left: "center" },
    tooltip: { trigger: "axis" },
    xAxis: { type: "category", data: data?.months || [] },
    yAxis: { type: "value" },
    series: [
      { data: data?.pagu || [], type: "line", name: "Pagu Asli", smooth: true, itemStyle: { color: "#0D5CBD" } },
      { data: data?.p90 || [], type: "line", name: "P90 (Wajar)", smooth: true, itemStyle: { color: "#8A63E8" }, lineStyle: { type: "dashed" } },
    ]
  };
  return <ReactECharts option={options} style={{ height: "100%", width: "100%" }} />;
}
