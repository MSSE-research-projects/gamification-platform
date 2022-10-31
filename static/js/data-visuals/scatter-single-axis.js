// import * as echarts from 'echarts';
console.log("part_data", part_data);

var app = {};
for (var i = 0; i < mockData.length; i++) {
    var sectionData = mockData[i];
    var sectionTitle = sectionData.section;
    for (var j = 0; j < sectionData.parts.length; j++) {
        var partData = sectionData.parts[j];
        var part_type = partData['part_type'];
        if (part_type == 'multi-choice') {
            var part_data = partData['part_data'];
            for (var k = 0; k < part_data.length; k++) {
                var part_data_inner = part_data[k];
                var part_data_title = part_data_inner['title'];
                var part_data_name = part_data_inner['name'];
                var part_data_type = part_data_inner['type'];
                var data = part_data_inner['data'];
                var options = part_data_inner['options'];

                console.log("part_data_name",'chart-container-' +  part_data_name);
                var chartDom = document.getElementById('chart-container-' + part_data_name);
                var myChart = echarts.init(chartDom);

                var option;
                // prettier-ignore
                // const hours = [
                //     'agree', 'disagree', 'rerw', 'asppds', '4a'
                // ];
                const hours = data['labels']
                // prettier-ignore
                const days = [];
                days.push(part_data_title);
                // const days = [
                //     'Saturday'
                // ];
                // prettier-ignore
                const sca_data_list = data['datasets'][0]['data'];
                const sca_data = [];
                for (var l = 0; l < sca_data_list.length; l++) {
                    sca_data.push([0, l, sca_data_list[l]]);
                }
                // const sca_data = [[0,0,1], [0,1,2]]
                console.log("sca_data", sca_data);
                
                const title = [];
                const singleAxis = [];
                const series = [];
                days.forEach(function (day, idx) {
                title.push({
                    textBaseline: 'middle',
                    top: ((idx + 0.5) * 100) / 7 + '%',
                    text: day
                });
                singleAxis.push({
                    left: 150,
                    type: 'category',
                    boundaryGap: false,
                    data: hours,
                    top: (idx * 100) / 7 + 5 + '%',
                    height: 100 / 7 - 10 + '%',
                    axisLabel: {
                    interval: 0
                    }
                });
                series.push({
                    singleAxisIndex: idx,
                    coordinateSystem: 'singleAxis',
                    type: 'scatter',
                    data: [],
                    symbolSize: function (dataItem) {
                    return dataItem[1] * 4; // 4
                    }
                });
                });
                sca_data.forEach(function (dataItem) {
                series[dataItem[0]].data.push([dataItem[1], dataItem[2]]);
                });
                option = {
                tooltip: {
                    position: 'top'
                },
                title: title,
                singleAxis: singleAxis,
                series: series
                };

                option && myChart.setOption(option);
            }
        }
    }
}