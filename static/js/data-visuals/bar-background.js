var chartDom = document.getElementById("bar-chart-container");
var myChart = echarts.init(chartDom,null,{height: 200});
var option;

option = {
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