$(function () {
  $.ajaxSetup({
    headers: { "X-CSRFToken": "{{ csrf_token }}" }
  });
});

var queTypeMap = {
  'mcq': 'MULTIPLECHOICE',
  'fixed-text': 'FIXEDTEXT',
  'multi-text': 'MULTIPLETEXT',
  'textarea': 'TEXTAREA',
  'number': 'NUMBER',
};
var queTypeMapRev = {
  'MULTIPLECHOICE': 'mcq',
  'FIXEDTEXT': 'fixed-text',
  'MULTIPLETEXT': 'multi-text',
  'TEXTAREA': 'textarea',
  'NUMBER': 'number',
};

getSurvey = function (survey_pk, options) {
  var survey = null;
  var artifact_question_pk;

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
      for (var i = 0; i < data.length; i++) {
        if (data[i].title == 'Artifact') {
          $.ajax({
            async: false,
            url: `/api/sections/${data[i].pk}/questions/`,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
              if (data.length > 0) {
                artifact_question_pk = data[0].pk;
              }
            },
          });
          continue;
        }

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
            for (var j = 0; j < data.length; j++) {
              var question = null;
              data[j].section = section;

              var questionClass = null;
              switch (data[j].question_type) {
                case 'MULTIPLECHOICE':
                  // Retrieve all choices
                  var choices = [];
                  $.ajax({
                    async: false,
                    url: `/api/questions/${data[j].pk}/options/`,
                    type: 'GET',
                    dataType: 'json',
                    success: function (data) {
                      for (var l = 0; l < data.length; l++) {
                        var choice = new OptionChoice(data[l]);
                        choices.push(choice);
                      }
                    }
                  });
                  data[j].choices = choices;

                  questionClass = MultipleChoiceQuestion;
                  break;
                case 'FIXEDTEXT':
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

                  questionClass = FixedTextInputQuestion;
                  break;
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

                  questionClass = MultiTextInputQuestion;
                  break;
                case 'TEXTAREA':
                  questionClass = TextAreaQuestion;
                  break;
                case 'NUMBER':
                  questionClass = NumericInputQuestion;
                  break;
                default:
                  break;
              }

              question = new questionClass(
                data[j],
                options = options
              );

              section.addQuestion(question);
            }
          }
        });

        survey.addSection(section);
      }
    }
  });

  return { survey, artifact_question_pk };
}

updateAnswers = function (survey, artifact_review_pk) {
  for (var i = 0; i < survey.sections.length; i++) {
    var section = survey.sections[i];
    for (var j = 0; j < section.questions.length; j++) {
      var question = section.questions[j];
      var answers = [];
      $.ajax({
        async: false,
        url: `/api/artifact_reviews/${artifact_review_pk}/questions/${question.pk}/answers/`,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
          data.map(({ answer_text }) => answers.push(answer_text));
        }
      });
      question.setAnswers(answers);
    }
  }
}

getArtifactReviews = function (artifact_review_pk, artifact_question_pk) {
  var reviews = {};
  $.ajax({
    async: false,
    url: `/api/artifact_reviews/${artifact_review_pk}/questions/${artifact_question_pk}/answers/`,
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      console.log(data);
      data.forEach(({ page, answer_text }) => {
        page = parseInt(page);
        reviews[page] = answer_text;
      });
    }
  });

  return reviews;
}
