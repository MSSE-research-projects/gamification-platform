$(function () {
  $.ajaxSetup({
    headers: { "X-CSRFToken": "{{ csrf_token }}" }
  });
});

var queTypeMap = {
  'mcq': 'MULTIPLECHOICE',
  'smcq': 'SCALEMULTIPLECHOICE',
  'fixed-text': 'FIXEDTEXT',
  'multi-text': 'MULTIPLETEXT',
  'textarea': 'TEXTAREA',
  'number': 'NUMBER',
};
var queTypeMapRev = {
  'MULTIPLECHOICE': 'mcq',
  'SCALEMULTIPLECHOICE': 'smcq',
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

  var surveyData = null;
  $.ajax({
    async: false,
    url: `/api/surveys/${survey_pk}/get_info/`,
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      surveyData = JSON.parse(data);
    }
  });

  var sectionData = surveyData.sections;

  survey = new Survey(
    surveyData,
    sections = [],
    options = options
  );

  sectionData.forEach(data => {
    if (data.title == 'Artifact') {
      artifact_question_pk = data.questions[0].pk;
      return;
    }

    var questionData = data.questions;

    data.survey = survey;
    var section = new Section(
      data,
      questions = [],
      options = options
    );

    questionData.forEach(data => {
      data.section = section;

      switch (data.question_type) {
        case 'MULTIPLECHOICE':
          // Retrieve all choices
          var choices = [];

          data.option_choices.forEach(choice => {
            choices.push(new OptionChoice(choice));
          });

          data.choices = choices;

          questionClass = MultipleChoiceQuestion;
          break;
        case 'SCALEMULTIPLECHOICE':
          var numberOfScale = data.number_of_scale;
          data.numberOfScale = numberOfScale;

          questionClass = ScaleMultipleChoiceQuestion;
          break;
        case 'FIXEDTEXT':
          var numberOfText = data.number_of_text;
          data.numberOfText = numberOfText;

          questionClass = FixedTextInputQuestion;
          break;
        case 'MULTIPLETEXT':
          var numberOfText = data.number_of_text;
          data.numberOfText = numberOfText;

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
        data,
        options = options
      );

      section.addQuestion(question);
    });

    survey.addSection(section);
  });

  return { survey, artifact_question_pk };
}

updateAnswers = function (survey, artifact_review_pk) {
  var ajaxCalls = [];
  for (var i = 0; i < survey.sections.length; i++) {
    var section = survey.sections[i];
    for (var j = 0; j < section.questions.length; j++) {
      var question = section.questions[j];
      var answers = [];

      var ajaxCall = (question, answers) => {
        return new Promise((resolve, reject) => {
          $.ajax({
            url: `/api/artifact_reviews/${artifact_review_pk}/questions/${question.pk}/answers/`,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
              data.map(({ answer_text }) => answers.push(answer_text));
              question.setAnswers(answers);
            }
          });
        });
      }

      ajaxCalls.push(ajaxCall(question, answers));
    }
  }

  Promise.all(ajaxCalls);
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
