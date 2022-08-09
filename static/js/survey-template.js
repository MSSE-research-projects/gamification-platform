// Helper functions

/**
 * @param {String} HTML representing a single element
 * @return {Element}
 */
function htmlToElement(html) {
  var template = document.createElement('template');
  html = html.trim(); // Never return a text node of whitespace as the result
  template.innerHTML = html;
  return template.content.firstChild;
}

/**
* @param {String} HTML representing any number of sibling elements
* @return {NodeList} 
*/
function htmlToElements(html) {
  var template = document.createElement('template');
  template.innerHTML = html;
  return template.content.childNodes;
}

/*******************************************/
/*********      Survey Class      **********/
/*******************************************/
class Survey {
  constructor(data = {}, sections = [], options = {}) {
    this.pk = data.pk;
    this.name = data.name;
    this.instructions = data.instructions;
    this.other_info = data.other_info;

    this.sections = sections;
    this.options = options;

    this.buildElement();
  }

  on(event, selector, handler) {
    if (handler == null) {
      handler = selector;
      selector = null;
      $(this.element).on(event, handler.bind(this));
    } else {
      $(this.element).on(event, selector, handler.bind(this));
    }
  }


  // Functions for building the DOM element
  buildElement() {
    this.element = this._buildWrapperElement();
    if (this.options.preview) {
      this.headerElement = this._buildPreviewHeaderElement();
    } else if (this.options.editable) {
      this.headerElement = this._buildEditableHeaderElement();
    } else {
      this.headerElement = this._buildNormalHeaderElement();
    }
    this.sectionElement = this._buildSectionElement();

    $(this.element).find('.card-body').append(this.headerElement);
    $(this.element).find('.card-body').append(this.sectionElement);

    if (this.options.live) {
      this.footerElement = this._buildFooterElement();
      $(this.element).find('.card-body').append(this.footerElement);
    }
  }

  _buildWrapperElement() {
    var html = '';
    html += '<div class="card survey">';
    html += '  <div class="card-body">';
    html += '  </div>';
    html += '</div>';

    return htmlToElement(html);
  }

  _buildNormalHeaderElement() {
    var html = '';
    html += '<div class="survey-header row mb-3 align-items-center justify-content-between">';
    html += '  <div class="col-md-6 col-sm-12 text-start">';
    html += '    <h2 class="card-title survey-name">' + this.name + '</h2>';
    html += '    <p class="card-description survey-instructions">' + this.instructions + '</p>';
    html += '  </div>';
    html += '  <div class="col-md-3 col-sm-12 text-end">';
    html += '    <button class="btn btn-primary artifact-preview-btn" data-bs-toggle="modal" data-bs-target="#artifactPreviewModal">';
    html += '      Artifact Preview';
    html += '    </button>';
    html += '  </div>';
    html += '</div>';

    return htmlToElement(html);
  }

  _buildPreviewHeaderElement() {
    var html = '';
    html += '<div class="survey-header row mb-3 align-items-center justify-content-between">';
    html += '  <div class="col-md-6 col-sm-12 text-start">';
    html += '    <h2 class="card-title survey-name">' + this.name + '</h2>';
    html += '    <p class="card-description survey-instructions">' + this.instructions + '</p>';
    html += '  </div>';
    html += '  <div class="col-md-3 col-sm-12 text-end">';
    html += '    <button class="btn btn-primary artifact-preview-btn" data-bs-toggle="modal" data-bs-target="#artifactPreviewModal">';
    html += '      Artifact Preview';
    html += '    </button>';
    html += '  </div>';
    html += '  <div class="col-md-3 col-sm-12 text-end">';
    html += '    <button class="btn btn-primary back-btn">';
    html += '      Back';
    html += '    </button>';
    html += '  </div>';
    html += '</div>';

    return htmlToElement(html);
  }

  _buildEditableHeaderElement() {
    var html = '';
    html += '<div class="survey-header row mb-3 align-items-center justify-content-between">';
    html += '  <div class="col-md-6 col-sm-12 text-start">';
    html += '    <h2 class="card-title survey-name">' + this.name + '</h2>';
    html += '    <p class="card-description survey-instructions">' + this.instructions + '</p>';
    html += '  </div>';
    html += '  <div class="col-md-2 col-sm-12 text-end">';
    html += '    <button class="btn btn-secondary edit-template-btn">';
    html += '      <i class="fa fa-edit"></i> Edit Template';
    html += '    </button>';
    html += '  </div>';
    html += '  <div class="col-md-2 col-sm-12 text-end">';
    html += '    <button class="btn btn-secondary student-view-btn">';
    html += '      <i class="fa fa-glasses"></i> Student View';
    html += '    </button>';
    html += '  </div>';
    html += '  <div class="col-md-2 col-sm-12 text-end">';
    html += '    <button class="btn btn-primary add-section-btn" data-bs-toggle="modal" data-bs-target="#addSectionModal">';
    html += '      <i class="fa fa-plus"></i> Add Section';
    html += '    </button>';
    html += '  </div>';
    html += '</div>';

    return htmlToElement(html);
  }

  _buildSectionElement() {
    var div = document.createElement('div');
    div.classList.add('survey-sections');
    for (var i = 0; i < this.sections.length; i++) {
      var section = this.sections[i];
      div.appendChild(section.element);
    }
    return div;
  }

  _buildFooterElement() {
    var html = '';
    html += '<div class="survey-footer row mb-3 align-items-center justify-content-between">';
    html += '  <div class="d-grid col text-end">';
    html += '    <button class="btn btn-primary submit-survey-btn">';
    html += '      <i class="fa fa-arrow-circle-right"></i> Submit Survey';
    html += '    </button>';
    html += '  </div>';
    html += '</div>';

    return htmlToElement(html);
  }

  // Functions for manipulating the survey
  updateElement() {
    $(this.element).find('.survey-name').text(this.name);
    $(this.element).find('.survey-instructions').text(this.instructions);
  }

  addSection(section) {
    this.sections.push(section);
    this.sectionElement.appendChild(section.element);
  }

  addSectionByTitle(title, description) {
    var section = new Section(title, description);
    this.addSection(section);
  }

  removeSection(section) {
    this.sections.splice(this.sections.indexOf(section), 1);
    this.sectionElement.removeChild(section.element);
  }

  removeSectionByTitle(title) {
    var section = this.getSectionByTitle(title);
    this.removeSection(section);
  }

  removeSectionByIndex(index) {
    var section = this.sections[index];
    this.removeSection(section);
  }

  getSectionByTitle(title) {
    return this.sections.find(function (section) {
      return section.title === title;
    });
  }

  getSectionByIndex(index) {
    return this.sections[index];
  }

  getSections() {
    return this.sections;
  }

  render(e) {
    e.appendChild(this.element);
  }
}


/*******************************************/
/*********      Section Class      *********/
/*******************************************/
class Section {
  constructor(data = {}, questions = [], options = {}) {
    this.pk = data.pk;
    this.title = data.title;
    this.description = data.description;
    this.is_required = data.is_required;
    this.survey = data.survey;

    this.questions = questions;
    this.options = options;

    this.buildElement();
  }

  on(event, selector, handler) {
    if (handler == null) {
      handler = selector;
      selector = null;
      $(this.element).on(event, handler.bind(this));
    } else {
      $(this.element).on(event, selector, handler.bind(this));
    }
  }

  // Functions for building the DOM element
  buildElement() {
    this.element = this._buildWrapperElement();
    this.headerElement;
    if (this.options.editable) {
      this.headerElement = this._buildEditableHeaderElement();
    } else {
      this.headerElement = this._buildNormalHeaderElement();
    }
    this.questionElement = this._buildQuestionElement();

    this.element.appendChild(this.headerElement);
    this.element.appendChild(this.questionElement);

    if (this.options.live) {
      this.footerElement = this._buildFooterElement();
      this.element.appendChild(this.footerElement);
    }
  }

  _buildWrapperElement() {
    var html = '';
    html += '<fieldset class="section">';
    // html += `  <legend class="section-title">${this.title}${this.is_required ? '' : ' - Optional'}</legend>`;
    html += `  <legend class="section-title">${this.title}</legend>`;
    html += '</fieldset>';

    return htmlToElement(html);
  }

  _buildNormalHeaderElement() {
    var html = '';
    html += '<div class="section-header">';
    html += '  <p class="card-description section-description">' + this.description + '</p>';
    html += '</div>';

    return htmlToElement(html);
  }

  _buildEditableHeaderElement() {
    var html = '';
    html += '<div class="section-header row mb-3 align-items-center justify-content-between">';
    html += '  <div class="col-md-9 col-sm-12 text-start">';
    html += '    <p class="card-description section-description">' + this.description + '</p>';
    html += '  </div>';
    html += '  <div class="col-md-3 col-sm-12 text-end">';
    html += '    <button type="button" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#addQuestionModal"><i class="fa fa-plus"></i></button>';
    html += '      <button type="button" class="btn btn-sm btn-warning" data-bs-toggle="modal" data-bs-target="#editSectionModal"><i class="fa fa-edit"></i></button>';
    html += '    <button type="button" class="btn btn-sm btn-danger remove-section-btn"><i class="fa fa-trash"></i></button>';
    html += '  </div>';
    html += '</div>';

    return htmlToElement(html);
  }

  _buildQuestionElement() {
    var div = document.createElement('div');
    div.classList.add('section-questions');
    for (var i = 0; i < this.questions.length; i++) {
      var question = this.questions[i];
      div.appendChild(htmlToElement('<hr>'));
      div.appendChild(question.element);
    }
    return div;
  }

  _buildFooterElement() {
    var html = '';
    html += '<div>';
    html += '  <hr>';
    html += '  <div class="section-footer row mb-3 align-items-center justify-content-between">';
    html += '    <div class="col text-end">';
    html += '      <button type="button" class="btn btn-sm btn-primary save-section-btn"><i class="fa fa-save"></i> Save</button>';
    html += '    </div>';
    html += '  </div>';
    html += '</div>';

    return htmlToElement(html);
  }

  // Functions for manipulating the section
  updateElement() {
    $(this.element).find('.section-title').text(this.title);
    $(this.headerElement).find('.section-description').text(this.description);
  }

  getQuestionByText(text) {
    return this.questions.find(function (question) {
      return question.text === text;
    });
  }

  addQuestion(question) {
    this.questions.push(question);
    this.questionElement.appendChild(htmlToElement('<hr>'));
    this.questionElement.appendChild(question.element);
  }

  removeQuestion(question) {
    this.questions.splice(this.questions.indexOf(question), 1);
    this.questionElement.removeChild(question.element.previousElementSibling);
    this.questionElement.removeChild(question.element);
  }

  removeQuestionByText(text) {
    var question = this.getQuestionByText(text);
    this.removeQuestion(question);
  }
};


/*******************************************/
/*********     Question Class      *********/
/*******************************************/
class OptionChoice {
  constructor(data = {}) {
    this.pk = data.pk;
    this.text = data.text;
    if (data.value == undefined) {
      this.value = data.text;
    } else {
      this.value = data.value;
    }

    this.question = data.question;
  }
}


class Question {
  constructor(data = {}, options = {}) {
    this.pk = data.pk;
    this.text = data.text;
    this.section = data.section;

    this.options = options;

    if (new.target === Question) {
      throw new TypeError('Cannot construct Question instances directly');
    }

    if (this._buildWrapperElement == undefined) {
      throw new TypeError('Question subclass must implement _buildWrapperElement');
    }
    if (this._buildTextElement == undefined) {
      throw new TypeError('Question subclass must implement _buildTextElement');
    }
    if (this._buildOptionElement == undefined) {
      throw new TypeError('Question subclass must implement _buildOptionElement');
    }
  }

  on(event, selector, handler) {
    if (handler == null) {
      handler = selector;
      selector = null;
      $(this.element).on(event, handler.bind(this));
    } else {
      $(this.element).on(event, selector, handler.bind(this));
    }
  }

  // Functions for building the DOM element
  buildElement() {
    this.element = this._buildWrapperElement();
    this.textElement = this._buildTextElement();
    this.optionElement = this._buildOptionElement();

    this.element.appendChild(this.textElement);
    this.element.appendChild(this.optionElement);

    if (this.options.editable) {
      this.editElement = this._buildEditElement();
      this.element.appendChild(this.editElement);
    }
  }

  _buildEditElement() {
    var html = '';
    html += '<div class="col-lg-2 col-xxl-1 text-end">';
    html += '  <button type="button" class="btn btn-sm btn-warning edit-quetions-btn" data-bs-toggle="modal" data-bs-target="#editQuestionModal"><i class="fa fa-edit"></i></button>';
    html += '  <button type="button" class="btn btn-sm btn-danger remove-question-btn"><i class="fa fa-trash"></i></button>';
    html += '</div>';

    return htmlToElement(html);
  }

  updateElement() {
    $(this.textElement).text(this.text);

    this.optionElement = this._buildOptionElement();
    $(this.element).find('.question-option').replaceWith(this.optionElement);
  }
}

class InlineStyleQuestion extends Question {
  constructor(data = {}, options = {}) {
    super(data, options);

    if (new.target === InlineStyleQuestion) {
      throw new TypeError('Cannot construct InlineStyleQuestion instances directly');
    }

    if (this._buildOption == undefined) {
      throw new TypeError('InlineStyleQuestion subclass must implement _buildOption');
    }
  }

  _buildWrapperElement() {
    var html = '';
    html += '<div class="question row mb-3 align-items-center justify-content-center">';
    html += '</div>';

    return htmlToElement(html);
  }

  _buildTextElement() {
    var html = '';
    html += '<label class="question-text col-lg-4 col-xxl-6 col-form-label">' + this.text + '</label>';

    return htmlToElement(html);
  }

  _buildOptionElement() {
    var html = '';
    html += '<div class="question-option col">';
    html += '</div>';

    var optionWrapper = htmlToElement(html);

    optionWrapper.appendChild(this._buildOption());

    return optionWrapper;
  }
}

class DefaultStyleQuestion extends Question {
  constructor(data = {}, options = {}) {
    super(data, options);

    if (new.target === DefaultStyleQuestion) {
      throw new TypeError('Cannot construct DefaultStyleQuestion instances directly');
    }

    if (this._buildOption == undefined) {
      throw new TypeError('DefaultStyleQuestion subclass must implement _buildOption');
    }
  }

  buildElement() {
    if (this.options.editable) {

      function _buildQuestionContentElement() {
        var html = '';
        html += '<div class="question-content col-lg-10 col-xxl-11">';
        html += '</div>';

        return htmlToElement(html);
      }

      this.element = this._buildWrapperElement();
      this.textElement = this._buildTextElement();
      this.optionElement = this._buildOptionElement();
      this.editElement = this._buildEditElement();

      this.questionContentElement = _buildQuestionContentElement();
      this.questionContentElement.appendChild(this.textElement);
      this.questionContentElement.appendChild(this.optionElement);

      this.element.appendChild(this.questionContentElement);
      this.element.appendChild(this.editElement);
    } else {
      super.buildElement();
    }
  }

  _buildWrapperElement() {
    var html = '';
    html += '<div class="question row mb-3 align-items-center justify-content-center">';
    html += '</div>';

    return htmlToElement(html);
  }

  _buildTextElement() {
    var html = '';
    html += '<label class="question-text form-label">' + this.text + '</label>';

    return htmlToElement(html);
  }

  _buildOptionElement() {
    var html = '';
    html += '<div class="question-option">';
    html += '</div>';

    var optionWrapper = htmlToElement(html);

    optionWrapper.appendChild(this._buildOption());

    return optionWrapper;
  }
}

// class GridStyleQuestion extends Question {
//   constructor(data = {}, options = {}) {
//     super(data, options);

//     if (new.target === GridStyleQuestion) {
//       throw new TypeError('Cannot construct GridStyleQuestion instances directly');
//     }

//     if (this._buildOption == undefined) {
//       throw new TypeError('GridStyleQuestion subclass must implement _buildOption');
//     }
//   }

//   _buildWrapperElement() {
//     var html = '';
//     html += '<div class="row mb-3 align-items-center justify-content-center">';
//     html += '</div>';

//     return htmlToElement(html);
//   }

//   _buildTextElement() {
//     var html = '';
//     html += '<label class="question-text col-auto form-label">' + this.text + '</label>';

//     return htmlToElement(html);
//   }

//   _buildOptionElement() {
//     var html = '';
//     html += '<input type="number" min="1" max="10" step="1" class="question-option col form-control">';

//     return htmlToElement(html);
//   }
// }



class MultipleChoiceQuestion extends InlineStyleQuestion {
  constructor(data = {}, options = {}) {
    super(data, options);
    this.choices = data.choices ? data.choices : [];
    this.type = 'mcq';

    this.buildElement();
  }

  _buildOption() {
    var randomString = Math.random().toString(36).substring(2, 15);
    var html = '';
    html += '<div class="row">';
    for (var i = 0; i < this.choices.length; i++) {
      html += '  <div class="col-sm">';
      html += '    <div class="form-check">';
      html += `      <input class="form-check-input" type="radio" name="${randomString}" value="${this.choices[i].value}">`;
      html += `      <label class="form-check-label">${this.choices[i].text}</label>`;
      html += '    </div>';
      html += '  </div>';
    }
    html += '</div>';

    return htmlToElement(html);
  }

  setAnswers(values) {
    for (var i = 0; i < values.length; i++) {
      $(this.element).find(`input[value="${values[i]}"]`).prop('checked', true);
    }
  }

  getAnswers() {
    // Get all chekced buttons
    var checkedButtons = $(this.element).find('input:checked');
    var answers = [];
    for (var i = 0; i < checkedButtons.length; i++) {
      answers.push(checkedButtons[i].value);
    }
    return answers;
  }

  getChoiceByText(text) {
    return this.choices.find(function (choice) {
      return choice.text === text;
    });
  }

  addChoice(choice) {
    this.choices.push(choice);

    this.updateElement();
  }

  addChoiceByText(text) {
    var choice = new OptionChoice(text);
    this.addChoice(choice);
  }

  removeChoice(choice) {
    this.choices.splice(this.choices.indexOf(choice), 1);

    this.updateElement();
  }

  removeChoiceByText(text) {
    var choice = this.getChoiceByText(text);
    this.removeChoice(choice);
  }
}

class FixedTextInputQuestion extends DefaultStyleQuestion {
  constructor(data = {}, options = {}) {
    super(data, options);
    this.placeholder = data.placeholder ? data.placeholder : '';
    this.numberOfText = data.numberOfText ? data.numberOfText : 1;
    this.type = 'text';

    this.buildElement();
  }

  _buildOption() {
    var html = '';
    html += '<div>';
    for (var i = 0; i < this.numberOfText; i++) {
      if (i === 0) {
        html += '<input type="text" class="form-control mb-2" placeholder="' + this.placeholder + '">';
      } else {
        html += '<input type="text" class="form-control mb-2">';
      }
    }
    html += '</div>';

    return htmlToElement(html);
  }

  setAnswers(values) {
    for (var i = 0; i < values.length; i++) {
      $(this.element).find('input')[i].value = values[i];
    }
  }

  getAnswers() {
    var inputs = $(this.element).find('input');
    var answers = [];
    for (var i = 0; i < inputs.length; i++) {
      if (inputs[i].value) {
        answers.push(inputs[i].value);
      }
    }
    return answers;
  }
}

class MultiTextInputQuestion extends DefaultStyleQuestion {
  constructor(data = {}, options = {}) {
    super(data, options);
    this.placeholder = data.placeholder ? data.placeholder : '';
    this.numberOfText = data.numberOfText ? data.numberOfText : 1;
    this.type = 'text';

    this.buildElement();

    this.on('click', '.add-text-input-btn', this.addTextInput.bind(this));
    this.on('click', '.remove-text-input-btn', this.removeTextInput.bind(this));
  }

  buildElement() {
    super.buildElement();

    if (!this.options.editable) {
      var footerElement = this._buildFooterElement();
      this.element.appendChild(footerElement);
    }
  }

  _buildOption() {
    var html = '';
    html += '<div class="text-lines">';
    for (var i = 0; i < this.numberOfText; i++) {
      if (i === 0) {
        html += '<input type="text" class="form-control mb-2" placeholder="' + this.placeholder + '">';
      } else {
        html += '<input type="text" class="form-control mb-2">';
      }
    }
    html += '</div>';

    return htmlToElement(html);
  }

  _buildFooterElement() {
    var html = '';
    html += '<div class="col text-end">';
    html += '  <button type="button" class="btn btn-sm btn-primary add-text-input-btn"><i class="fa fa-plus"></i> Add New Line</button>';
    html += '</div>';

    return htmlToElement(html);
  }

  addTextInput() {
    $(this.element).find('.text-lines').append(
      '<div class="input-group mb-2">' +
      '  <input type="text" class="form-control">' +
      '  <button class="btn btn-outline-danger remove-text-input-btn" type="button">Remove</button>' +
      '</div>'
    );
  }

  removeTextInput(event) {
    var button = $(event.currentTarget);
    button.closest('.input-group').remove();
  }

  setAnswers(values) {
    for (var i = 0; i < values.length; i++) {
      if (i >= this.numberOfText) {
        this.addTextInput();
      }
      $(this.element).find('input')[i].value = values[i];
    }
  }

  getAnswers() {
    var inputs = $(this.element).find('input');
    var answers = [];
    for (var i = 0; i < inputs.length; i++) {
      if (inputs[i].value) {
        answers.push(inputs[i].value);
      }
    }
    return answers;
  }
}

class TextAreaQuestion extends DefaultStyleQuestion {
  constructor(data = {}, options = {}) {
    super(data, options);
    this.placeholder = data.placeholder ? data.placeholder : '';
    this.numberOfText = data.numberOfText ? data.numberOfText : 5;
    this.type = 'text';

    this.buildElement();
  }

  _buildOption() {
    var html = '';
    html += '<textarea class="form-control" rows="' + this.numberOfText + '" placeholder="' + this.placeholder + '"></textarea>';

    return htmlToElement(html);
  }

  setAnswer(value) {
    $(this.element).find('textarea').val(value);
  }

  getAnswers() {
    var answer = $(this.element).find('textarea').val();
    return answer;
  }
}

class NumericInputQuestion extends InlineStyleQuestion {
  constructor(data = {}, options = {}) {
    super(data, options);
    this.minValue = data.minValue ? data.minValue : 1;
    this.maxValue = data.maxValue ? data.maxValue : 10;
    this.step = data.step ? data.step : 1;
    this.type = 'number';

    this.buildElement();
  }

  _buildOption() {
    var html = '';
    // html += '<div>';
    html += `<input type="number" min="${this.minValue}" max="${this.maxValue}" step="${this.step}" class="col form-control">`;
    // html += '</div>';

    return htmlToElement(html);
  }

  getAnswers() {
    var inputs = $(this.element).find('input');
    var answers = [];
    for (var i = 0; i < inputs.length; i++) {
      answers.push(inputs[i].value);
    }
    return answers;
  }
}


/*******************************************/
/*********      Section Modal      *********/
/*******************************************/

class SectionModal {
  constructor(modal) {
    this.modal = modal;
  }

  reset() {
    this.modal.find('#sectionTitle').val('');
    this.modal.find('#sectionDescription').val('');
  }

  hide() {
    this.modal.modal('hide');
  }

  show() {
    this.modal.modal('show');
  }

  on(event, selector, handler) {
    if (handler == null) {
      handler = selector;
      selector = null;
      this.modal.on(event, handler.bind(this));
    } else {
      this.modal.on(event, selector, handler.bind(this));
    }
  }
}


/*******************************************/
/*********     Question Modal      *********/
/*******************************************/

class QuestionModal {
  constructor(modal) {
    this.modal = modal;

    this.on('change', '#questionType', () => this.toggleQuestionTypeFields());
    this.on('click', '.add-option-btn', () => this.addMcqOption());
    this.on('click', '.remove-option-btn', (event) => this.removeMcqOption(event));

    this.modal.find('#questionType').val('');
    this.modal.find('#questionType').trigger('change');
  }

  toggleQuestionTypeFields() {
    var questionType = this.modal.find('#questionType').val();
    switch (questionType) {
      case 'mcq':
        this.modal.find('#mcqFields').show();
        this.modal.find('#textFields').hide();
        break;
      case 'fixed-text':
      case 'multi-text':
        this.modal.find('#mcqFields').hide();
        this.modal.find('#textFields').show();
        break;
      default:
        this.modal.find('#mcqFields').hide();
        this.modal.find('#textFields').hide();
        break;
    }
  }

  addMcqOption() {
    this.modal.find('#choices').append(
      '<div class="input-group mb-2">' +
      '  <input type="text" class="form-control" placeholder="New Option" required>' +
      '  <button class="btn btn-outline-danger remove-option-btn" type="button">Remove</button>' +
      '</div>'
    );
  }

  removeMcqOption(event) {
    var button = $(event.currentTarget);
    button.closest('.input-group').remove();
  }

  hide() {
    this.modal.modal('hide');
  }

  show() {
    this.modal.modal('show');
  }

  reset() {
    this.modal.find('#sectionTitleInQuestionModal').val('');
    this.modal.find('#questionText').val('');
    this.modal.find('#questionType').val('');
    this.modal.find('#questionType').trigger('change');
    // Reset MCQ Options fields
    this.modal.find('#choices').html(
      '<input type="text" class="form-control mb-2" id="mcqOptions" placeholder="New Option" required>'
    );
    this.modal.find('#mcqOptions').val('');
    // Reset the number of blanks in text fields
    this.modal.find('#numberOfText').val('');
  }

  on(event, selector, handler) {
    // Overload the function to accept an optional selector and handler
    // If the handler is null, the selector is assumed to be the handler
    if (handler == null) {
      handler = selector;
      selector = null;
      this.modal.on(event, handler.bind(this)); // Bind the handler to the modal
    } else {
      this.modal.on(event, selector, handler.bind(this)); // Bind the handler to the modal
    }
  }
}
