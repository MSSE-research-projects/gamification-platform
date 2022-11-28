var chartDom = document.getElementById("bar-chart-container");
var myChart = echarts.init(chartDom, null, { height: 400 });
var option;

option = {
  visualMap: [
    {
      show: true,
      top: "10%",
      type: "continuous",
      dimension: 1,
      min: 0,
      max: 10,
      inRange: {
        color: ["red", "light green"],
      },
    },
  ],
  xAxis: {
    type: "category",
    data: scoreLabels,
  },
  yAxis: {
    type: "value",
  },
  series: [
    {
      data: scoreData,
      barWidth: 50,
      label: {
        show: true,
        position: "insideTop",
        formatter: "{c}",
        color: "#000000",
      },

      type: "bar",
      showBackground: true,
      backgroundStyle: {
        color: "rgba(180, 180, 180, 0.2)",
      },
    },
  ],
};

option && myChart.setOption(option);
window.addEventListener("resize", myChart.resize);
