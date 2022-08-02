$(function () {
  $.ajaxSetup({
    headers: { "X-CSRFToken": "{{ csrf_token }}" }
  });
});

var queTypeMap = {
  'mcq': 'MULTIPLECHOICE',
  'text': 'FIXEDTEXT',
  'textarea': 'FIXEDTEXT',
};
var queTypeMapRev = {
  'MULTIPLECHOICE': 'mcq',
  'FIXEDTEXT': 'text',
};

getSurvey = function (survey_pk, options) {
  var survey = null;

  if (options.preview) {
    options.editable = false;
    options.live = false;
  }

  $.ajax({
    async: false,
    url: `/api/surveys/${survey_pk}/`,
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      // console.log(data);
      survey = new Survey(
        data,
        sections = [],
        options = options
      );
    }
  });

  $.ajax({
    async: false,
    url: `/api/surveys/${survey.pk}/sections/`,
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      // console.log(data);
      for (var i = 0; i < data.length; i++) {
        data[i].survey = survey;
        var section = new Section(
          data[i],
          questions = [],
          options = options
        );

        $.ajax({
          async: false,
          url: `/api/sections/${section.pk}/questions/`,
          type: 'GET',
          dataType: 'json',
          success: function (data) {
            // console.log(data);
            for (var j = 0; j < data.length; j++) {
              var question = null;
              data[j].section = section;
              switch (data[j].question_type) {
                case 'MULTIPLECHOICE':
                  var choices = [];
                  $.ajax({
                    async: false,
                    url: `/api/questions/${data[j].pk}/options/`,
                    type: 'GET',
                    dataType: 'json',
                    success: function (data) {
                      // console.log(data);
                      for (var l = 0; l < data.length; l++) {
                        var choice = new OptionChoice(data[l]);
                        choices.push(choice);
                      }
                    }
                  });
                  data[j].choices = choices;
                  question = new MultipleChoiceQuestion(
                    data[j],
                    options = options
                  );
                  break;
                case 'FIXEDTEXT':
                case 'MULTIPLETEXT':
                  var numberOfText;
                  $.ajax({
                    async: false,
                    url: `/api/questions/${data[j].pk}/options/`,
                    type: 'GET',
                    dataType: 'json',
                    success: function (data) {
                      if (data.length > 0) {
                        numberOfText = data[0].number_of_text;
                      } else {
                        numberOfText = 1;
                      }
                    }
                  });
                  data[j].numberOfText = numberOfText;
                  question = new TextInputQuestion(
                    data[j],
                    options = options
                  );
                  break;
                default:
                  break;
              }
              section.addQuestion(question);
            }
          }
        });

        survey.addSection(section);
      }
    }
  });

  return survey;
}
