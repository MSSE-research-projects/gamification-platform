var chartDom = document.getElementById("tree-map-container-" + aspect_name);
var myChart = echarts.init(chartDom);
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
          color: ["#942e38", "#aaa", "#269f3c"],
          colorMappingBy: "value",
          itemStyle: {
            gapWidth: 1,
          },
        },
      ],
      data: [
        {
          name: "Great",
          value: 1,
          children: [
            {
              name: "Negative",
              value: 6,
              children: [
                {
                  name: "clear",
                  value: 2,
                },
                {
                  name: "friendly",
                  value: 2,
                },
                {
                  name: "comes with images",
                  value: 1,
                },
                {
                  name: "data-driven",
                  value: 1,
                },
              ],
            },

            {
              name: "little lengthy",
              value: 1,
            },
            {
              name: "abrupt end",
              value: 1,
            },
            {
              name: "more interactions",
              value: 1,
            },
          ],
        },
      ],
    },
  ],
};

option && myChart.setOption(option);
window.addEventListener("resize", myChart.resize);
