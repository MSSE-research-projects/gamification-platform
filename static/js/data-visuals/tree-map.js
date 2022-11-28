var chartDom = document.getElementById("tree-map-container");
var myChart = echarts.init(chartDom,null,{height: 400});
var option;

option = {
  title: {
    text: "Top Tags from other reviewers",
    left: "center",
  },
  itemStyle: {
    borderWidth: 0,
    gapWidth: 5,
  },
  tooltip: {},

  series: [
    {
      type: "treemap",
      levels: [
        {
          itemStyle: {
            borderWidth: 3,
            borderColor: "#333",
            gapWidth: 3,
          },
        },
        {
          colorMappingBy: "value",
          itemStyle: {
            gapWidth: 1,
          },
        },
      ],
      data: treeData,
      
    },
  ],
};

option && myChart.setOption(option);
window.addEventListener("resize", myChart.resize);