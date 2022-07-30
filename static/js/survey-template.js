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
  constructor(name = '', instructions = '', sections = [], options = {}) {
    this.name = name;
    this.instructions = instructions;
    this.sections = sections;
    this.options = options;

    this.buildElement();

    // Redirect to student view page
    $(this.element).find('.student-view-btn').on('click', function () {
      window.location.href = '/test_view_survey/';
    }.bind(this));
  }

  // Set Database pk
  setPk(pk) {
    this.pk = pk;
  }

  // Functions for building the DOM element
  buildElement() {
    this.element = this._buildWrapperElement();
    this.headerElement = this._buildHeaderElement();
    this.editableHeaderElement = this._buildEditableHeaderElement();
    this.sectionElement = this._buildSectionElement();

    if (this.options.edit) {
      $(this.element).find('.card-body').append(this.editableHeaderElement);
    } else {
      $(this.element).find('.card-body').append(this.headerElement);
    }
    $(this.element).find('.card-body').append(this.sectionElement);
  }

  _buildWrapperElement() {
    var html = '';
    html += '<div class="card">';
    html += '  <div class="card-body">';
    html += '  </div>';
    html += '</div>';

    return htmlToElement(html);
  }

  _buildHeaderElement() {
    var html = '';
    html += '<h2 class="card-title">' + this.name + '</h2>';
    html += '<p class="card-description">' + this.instructions + '</p>';

    return htmlToElement(html);
  }

  _buildEditableHeaderElement() {
    var html = '';
    html += '<div class="row mb-3 align-items-center justify-content-between">';
    html += '  <div class="col-md-6 col-sm-12 text-start">';
    html += '    <h2 class="card-title">' + this.name + '</h2>';
    html += '    <p class="card-description">' + this.instructions + '</p>';
    html += '  </div>';
    html += '  <div class="col-md-3 col-sm-12 text-end">';
    html += '    <button class="btn btn-secondary student-view-btn">';
    html += '      <i class="fa fa-glasses"></i> Student View';
    html += '    </button>';
    html += '  </div>';
    html += '  <div class="col-md-3 col-sm-12 text-end">';
    html += '    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSectionModal">';
    html += '      <i class="fa fa-plus"></i> Add Section';
    html += '    </button>';
    html += '  </div>';
    html += '</div>';

    return htmlToElement(html);
  }

  _buildSectionElement() {
    var div = document.createElement('div');
    for (var i = 0; i < this.sections.length; i++) {
      var section = this.sections[i];
      section.registerEventOnRemove(this);
      div.appendChild(section.element);
    }
    return div;
  }

  // Functions for manipulating the survey
  addSection(section) {
    section.registerEventOnRemove(this);
    this.sections.push(section);
    this.sectionElement.appendChild(section.element);
  }

  addSectionByName(name, description) {
    var section = new Section(name, description);
    this.addSection(section);
  }

  updateElement() {
    this.buildElement();
  }

  removeSection(section) {
    this.sections.splice(this.sections.indexOf(section), 1);
    this.sectionElement.removeChild(section.element);
  }

  removeSectionByName(name) {
    var section = this.getSectionByName(name);
    this.removeSection(section);
  }

  removeSectionByIndex(index) {
    var section = this.sections[index];
    this.removeSection(section);
  }

  getSectionByName(name) {
    return this.sections.find(function (section) {
      return section.name === name;
    });
  }

  getSectionByIndex(index) {
    return this.sections[index];
  }

  render(e) {
    e.appendChild(this.element);
  }
}


/*******************************************/
/*********      Section Class      *********/
/*******************************************/
class Section {
  constructor(name = '', description = '', questions = [], options = {}) {
    this.name = name;
    this.description = description;
    this.questions = questions;
    this.options = options;

    this.buildElement();
  }

  // Set Database pk
  setPk(pk) {
    this.pk = pk;
  }

  // Functions for building the DOM element
  buildElement() {
    this.element = this._buildWrapperElement();
    this.headerElement = this._buildHeaderElement();
    this.editableHeaderElement = this._buildEditableHeaderElement();
    this.questionElement = this._buildQuestionElement();

    if (this.options.edit) {
      this.element.appendChild(this.editableHeaderElement);
    } else {
      this.element.appendChild(this.headerElement);
    }
    this.element.appendChild(this.questionElement);
  }

  _buildWrapperElement() {
    var html = '';
    html += '<fieldset class="section">';
    html += '  <legend>' + this.name + '</legend>';
    html += '</fieldset>';

    return htmlToElement(html);
  }

  _buildHeaderElement() {
    var html = '';
    html += '<p class="card-description">' + this.description + '</p>';

    return htmlToElement(html);
  }

  _buildEditableHeaderElement() {
    var html = '';
    html += '<div class="row mb-3 align-items-center justify-content-between">';
    html += '  <div class="col-md-9 col-sm-12 text-start">';
    html += '    <p class="card-description">' + this.description + '</p>';
    html += '  </div>';
    html += '  <div class="col-md-3 col-sm-12 text-end">';
    html += '    <button type="button" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#addQuestionModal"><i class="fa fa-plus"></i></button>';
    html += '      <button type="button" class="btn btn-sm btn-warning" data-bs-toggle="modal" data-bs-target="#editSectionModal"><i class="fa fa-edit"></i></button>';
    html += '    <button type="button" class="btn btn-sm btn-danger remove-sec-btn"><i class="fa fa-trash"></i></button>';
    html += '  </div>';
    html += '</div>';

    return htmlToElement(html);
  }

  _buildQuestionElement() {
    var div = document.createElement('div');
    for (var i = 0; i < this.questions.length; i++) {
      var question = this.questions[i];
      question.registerEventOnRemove(this);
      div.appendChild(question.element);
    }
    return div;
  }

  // Functions for manipulating the section
  getQuestionByText(text) {
    return this.questions.find(function (question) {
      return question.text === text;
    });
  }

  addQuestion(question) {
    question.registerEventOnRemove(this);
    this.questions.push(question);
    this.questionElement.appendChild(question.element);
  }

  removeQuestion(question) {
    this.questions.splice(this.questions.indexOf(question), 1);
    this.questionElement.removeChild(question.element);
  }

  removeQuestionByText(text) {
    var question = this.getQuestionByText(text);
    this.removeQuestion(question);
  }

  updateElement() {
    $(this.element).find('legend').text(this.name);
    $(this.headerElement).find('p.card-description').text(this.description);
    $(this.editableHeaderElement).find('p.card-description').text(this.description);
  }

  registerEventOnRemove(survey) {
    var self = this;
    $(this.element).find('.remove-sec-btn').on('click', function () {
      survey.removeSection(self);
    });
  }
};


/*******************************************/
/*********     Question Class      *********/
/*******************************************/
class Question {
  constructor(text = '', options = {}) {
    this.text = text;
    this.options = options;
  }

  // Set Database pk
  setPk(pk) {
    this.pk = pk;
  }

  // Functions for building the DOM element
  buildElement() {
    this.element = this._buildWrapperElement();
    this.textElement = this._buildTextElement();
    this.answerElement = this._buildAnswerElement();

    this.answerWrapperElement;
    this.answerWrapperElement = this._buildAnswerWrapperElement();

    this.element.appendChild(this.textElement);
    this.answerWrapperElement.appendChild(this.answerElement);
    this.element.appendChild(this.answerWrapperElement);

    if (this.options.edit) {
      this.element.appendChild(this._buildEditElement());
    }
  }

  _buildWrapperElement() {
    var html = '';
    html += '<div class="row mb-3 align-items-center justify-content-center question">';
    html += '</div>';

    return htmlToElement(html);
  }

  _buildTextElement() {
    var html = '';
    html += '<label class="col-lg-4 col-xxl-6 col-form-label">' + this.text + '</label>';

    return htmlToElement(html);
  }

  _buildAnswerWrapperElement() {
    var html = '';

    if (this.options.edit) {
      html += '<div class="col-lg-6 col-xxl-5">';
      html += '</div>';
    } else {
      html += '<div class="col-lg-8 col-xxl-6">';
      html += '</div>';
    }

    return htmlToElement(html);
  }

  _buildAnswerElement() {
    var html = '';
    return htmlToElement(html);
  }

  _buildEditElement() {
    var html = '';
    html += '<div class="col-lg-2 col-xxl-1 text-end">';
    html += '  <button type="button" class="btn btn-sm btn-warning edit-que-btn" data-bs-toggle="modal" data-bs-target="#editQuestionModal"><i class="fa fa-edit"></i></button>';
    html += '  <button type="button" class="btn btn-sm btn-danger remove-que-btn"><i class="fa fa-trash"></i></button>';
    html += '</div>';

    return htmlToElement(html);
  }

  updateElement() {
    $(this.textElement).text(this.text);

    this.answerElement = this._buildAnswerElement();
    this.answerWrapperElement.replaceChild(this.answerElement, this.answerWrapperElement.firstChild);
  }

  registerEventOnRemove(section) {
    var self = this;
    $(this.element).find('.remove-que-btn').on('click', function () {
      section.removeQuestion(self);
    });
  }
}

class MultipleChoiceQuestion extends Question {
  constructor(text = '', choices = [], options = {}) {
    super(text, options);
    this.choices = choices;
    this.type = 'mcq';

    this.buildElement();
  }

  _buildAnswerElement() {
    var html = '';
    html += '<div class="row">';
    for (var i = 0; i < this.choices.length; i++) {
      html += '  <div class="col-sm">';
      html += '    <div class="form-check">';
      html += '      <input class="form-check-input" type="radio" name="gridRadios" value="' + this.choices[i].value + '">';
      html += '      <label class="form-check-label">' + this.choices[i].text + '</label>';
      html += '    </div>';
      html += '  </div>';
    }
    html += '</div>';

    return htmlToElement(html);
  }
}

class TextInputQuestion extends Question {
  constructor(text = '', placeholder = '', displayLines = 1, options = {}) {
    super(text, options);
    this.placeholder = placeholder;
    this.displayLines = displayLines;
    this.type = 'text';

    this.buildElement();
  }

  _buildAnswerElement() {
    var html = '';
    html += '<div>';
    for (var i = 0; i < this.displayLines; i++) {
      if (i === 0) {
        html += '<input type="text" class="form-control" placeholder="' + this.placeholder + '">';
      } else {
        html += '<input type="text" class="form-control mt-2">';
      }
    }
    html += '</div>';

    return htmlToElement(html);
  }
}

class TextareaQuestion extends Question {
  constructor(text = '', placeholder = '', displayLines = 5, options = {}) {
    super(text, options);
    this.placeholder = placeholder;
    this.displayLines = displayLines;
    this.type = 'textarea';

    this.buildElement();
  }

  _buildAnswerElement() {
    var html = '';
    html += '    <textarea class="form-control" rows="' + this.displayLines + '" placeholder="' + this.placeholder + '"></textarea>';

    return htmlToElement(html);
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
    this.modal.find('#sectionName').val('');
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
      case 'text':
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
      '  <input type="text" class="form-control" placeholder="New Option">' +
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
    this.modal.find('#sectionNameInQuestionModal').val('');
    this.modal.find('#questionText').val('');
    this.modal.find('#questionType').val('');
    this.modal.find('#questionType').trigger('change');
    // Reset MCQ Options fields
    this.modal.find('#choices').html(
      '<input type="text" class="form-control mb-2" id="mcqOptions" placeholder="New Option">'
    );
    this.modal.find('#mcqOptions').val('');
    // Reset the number of blanks in text fields
    this.modal.find('#displayNum').val('');
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
