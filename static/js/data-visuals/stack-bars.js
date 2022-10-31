// var dom = document.getElementById('chart-container');
// console.log("part_data", part_data);
// var myChart = echarts.init(dom, null, {
//   renderer: 'canvas',
//   useDirtyRect: false
// });
// var app = {};

// var option;

// option = {
//   tooltip: {
//     trigger: 'axis',
//     axisPointer: {
//       // Use axis to trigger tooltip
//       type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
//     }
//   },
//   legend: {},
//   grid: {
//     left: '3%',
//     right: '4%',
//     bottom: '3%',
//     containLabel: true
//   },
//   xAxis: {
//     type: 'value'
//   },
//   yAxis: {
//     type: 'category',
//     data: ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5']
//   },
//   series: [
//     {
//       name: 'Strongly Disagree',
//       type: 'bar',
//       stack: 'total',
//       label: {
//         show: true
//       },
//       emphasis: {
//         focus: 'series'
//       },
//       data: [5,6,7,8,9]
//     },
//     {
//       name: 'Disagree',
//       type: 'bar',
//       stack: 'total',
//       label: {
//         show: true
//       },
//       emphasis: {
//         focus: 'series'
//       },
//       data: [5,2,7,6,9]
//     },
//     {
//       name: 'Neutral',
//       type: 'bar',
//       stack: 'total',
//       label: {
//         show: true
//       },
//       emphasis: {
//         focus: 'series'
//       },
//       data: [1,2,7,3,9]
//     },
//     {
//       name: 'Agree',
//       type: 'bar',
//       stack: 'total',
//       label: {
//         show: true
//       },
//       emphasis: {
//         focus: 'series'
//       },
//       data: [1,2,1,3,9]
//     },
//     {
//       name: 'Strongly Agree',
//       type: 'bar',
//       stack: 'total',
//       label: {
//         show: true
//       },
//       emphasis: {
//         focus: 'series'
//       },
//       data: [5,12,7,3,9]
//     }
//   ]
// };
// if (option && typeof option === 'object') {
//   myChart.setOption(option);
// }

// window.addEventListener('resize', myChart.resize);