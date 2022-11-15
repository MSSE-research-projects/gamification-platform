// chart_container_cnt
console.log("chart_container_cnt", chart_container_cnt);
// answers_fromAPI
console.log("answers_fromAPI::", answers_fromAPI);
var i = 0;
var labels = answers_fromAPI["label"];
console.log("labels", labels);
var sections = answers_fromAPI["sections"];

for (var section in sections) {
    var sectionData = sections[section];
    console.log("sectionData", sectionData);

    var questions = [];
    for (var question in sectionData) {
        questions.push(question + "\n");
    }
    console.log("questions", questions);

    var dom = document.getElementById('chart-container-' + i);
    var myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
    });
    var app = {};

    var option;
    
    option = {
        tooltip: {
            extraCssText: "width:400px; white-space:pre-wrap;position: absolute;",
            trigger: 'axis',
            confine: 'true',
            axisPointer: {
            // Use axis to trigger tooltip
            type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
            }
        },
        legend: {},
        grid: {
            top: '10%',
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            show:false,
            position: 'top',
            type: 'value'
        },
        yAxis: {
            type: 'category',
            data: questions,
            axisLabel: {
                margin: 40,
                width: "180",
                overflow: "break",
            },
        },
        series: []
    };

    for (var j = 0; j < labels.length; j++) {
        option_series_data = {
            name: labels[j],
            type: 'bar',
            stack: 'total',
            label: {
                show: true,
            },
            emphasis: {
                focus: 'series'
            },
            data: []
            }
        option.series.push(option_series_data);
    }
    j = 0;
    for (var question in sectionData) {  //j, k -> k, j
        var question_data = sectionData[question];  //[j]
        console.log("question_data", question_data);
        for (var k = 0; k < labels.length; k++) {
            option.series[k].data.push(question_data[k]);
        }
        j += 1;
    }

    if (option && typeof option === 'object') {
    myChart.setOption(option);
    }
    i += 1;
}
window.addEventListener('resize', myChart.resize);