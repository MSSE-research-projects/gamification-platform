var chartDom = document.getElementById("bar-chart-container-" + aspect_name);
var myChart = echarts.init(chartDom);
var option;

option = {
  xAxis: {
    type: "category",
    data: ["Content", "Design", "Delivery", "Overall"],
  },
  yAxis: {
    type: "value",
  },
  series: [
    {
      data: [5, 6, 4, 5],
      type: "bar",
      showBackground: true,
      backgroundStyle: {
        color: "rgba(180, 180, 180, 0.2)",
      },
    },
  ],
};

console.log("aspect_name" + aspect_name);

console.log("aspect_content" + aspect_content);

option && myChart.setOption(option);
window.addEventListener("resize", myChart.resize);
