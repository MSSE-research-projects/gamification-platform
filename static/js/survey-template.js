/*******************************************/
/*********      Survey Class      **********/
/*******************************************/
class Survey {
  constructor(name = '', instructions = '', sections = [], options = {}) {
    this.name = name;
    this.instructions = instructions;
    this.sections = sections;
    this.options = options;
  }

  addSection(section) {
    this.sections.push(section);
  }

  addSectionByName(name, description) {
    var section = new Section(name, description);
    this.sections.push(section);
  }

  removeSection(section) {
    var removedSection = this.sections.splice(this.sections.indexOf(section), 1);
    return removedSection;
  }

  removeSectionByName(name) {
    var section = this.getSectionByName(name);
    return this.removeSection(section);
  }

  removeSectionByIndex(index) {
    var section = this.sections[index];
    return this.removeSection(section);
  }

  getSectionByName(name) {
    return this.sections.find(function (section) {
      return section.name === name;
    });
  }

  getSectionByIndex(index) {
    return this.sections[index];
  }

  renderHTML() {
    var html = '';

    html += '<div class="card">';
    html += '  <div class="card-body">';
    if (this.options.edit) {
      html += '    <div class="row mb-3 align-items-center justify-content-between">';
      html += '      <div class="col-md-9 col-sm-12 text-start">';
      html += '        <h2 class="card-title">' + this.name + '</h2>';
      html += '        <p class="card-description">' + this.instructions + '</p>';
      html += '      </div>';
      html += '      <div class="col-md-3 col-sm-12 text-end">';
      html += '        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSectionModal">';
      html += '          <i class="fa fa-plus"></i> Add Section';
      html += '        </button>';
      html += '      </div>';
      html += '    </div>';
    } else {
      html += '    <h2 class="card-title">' + this.name + '</h2>';
      html += '    <p class="card-description">' + this.instructions + '</p>';
    }
    for (var i = 0; i < this.sections.length; i++) {
      html += this.sections[i].renderHTML();
    }
    html += '  </div>';
    html += '</div>';

    return html;
  }

  render(e) {
    var html = this.renderHTML();
    $(e).html(html);
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
  }

  getQuestionByText(text) {
    return this.questions.find(function (question) {
      return question.text === text;
    });
  }

  addQuestion(question) {
    this.questions.push(question);
  }

  removeQuestion(question) {
    var removedQuestion = this.questions.splice(this.questions.indexOf(question), 1);
    return removedQuestion;
  }

  removeQuestionByText(text) {
    var question = this.getQuestionByText(text);
    return this.removeQuestion(question);
  }

  renderHTML() {
    var html = '';

    html += '<fieldset>';
    html += '  <legend>' + this.name + '</legend>';
    if (this.options.edit) {
      html += '  <div class="row mb-3 align-items-center justify-content-between">';
      html += '    <div class="col-md-9 col-sm-12 text-start">';
      html += '      <p class="card-description">' + this.description + '</p>';
      html += '    </div>';
      html += '    <div class="col-md-3 col-sm-12 text-end">';
      html += '      <button type="button" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#addQuestionModal">Add Question</button>';
      html += '    </div>';
      html += '  </div>';
    } else {
      html += '  <p class="card-description">' + this.description + '</p>';
    }
    for (var i = 0; i < this.questions.length; i++) {
      html += this.questions[i].renderHTML();
    }
    html += '</fieldset>';

    return html;
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
}

class OptionChoice {
  constructor(text = '', value = '') {
    this.text = text;
    this.value = value;
  }
}

class MultipleChoiceQuestion extends Question {
  constructor(text = '', choices = [], options = {}) {
    super(text, options);
    this.choices = choices;
  }

  getChoiceByValue(value) {
    return this.choices.find(function (choice) {
      return choice.value === value;
    });
  }

  addChoice(choice) {
    this.choices.push(choice);
  }

  addChoiceByTextValue(text, value) {
    var choice = new OptionChoice(text, value);
    this.choices.push(choice);
  }

  removeChoice(choice) {
    var removedChoice = this.choices.splice(this.choices.indexOf(choice), 1);
    return removedChoice;
  }

  removeChoiceByValue(value) {
    var choice = this.getChoiceByValue(value);
    return this.removeChoice(choice);
  }

  renderHTML() {
    var html = '';

    html += '<div class="row mb-3 align-items-center justify-content-center">';
    html += '  <label class="col-sm-2 col-form-label">' + this.text + '</label>';
    html += '  <div class="col-sm-10">';
    html += '    <div class="row">';
    for (var i = 0; i < this.choices.length; i++) {
      html += '      <div class="col-sm">';
      html += '        <div class="form-check">';
      html += '          <input class="form-check-input" type="radio" name="gridRadios" value="' + this.choices[i].value + '">';
      html += '          <label class="form-check-label">' + this.choices[i].text + '</label>';
      html += '        </div>';
      html += '      </div>';
    }
    html += '    </div>';
    html += '  </div>';
    html += '</div>';

    return html;
  }
}

class TextInputQuestion extends Question {
  constructor(text = '', placeholder = '', displayLines = 1, options = {}) {
    super(text, options);
    this.placeholder = placeholder;
    this.displayLines = displayLines;
  }

  renderHTML() {
    var html = '';

    html += '<div class="row mb-3 align-items-center justify-content-center">';
    html += '  <label class="col-sm-2 col-form-label">' + this.text + '</label>';
    html += '  <div class="col-sm-10">';
    for (var i = 0; i < this.displayLines; i++) {
      if (i === 0) {
        html += '    <input type="text" class="form-control mb-2" placeholder="' + this.placeholder + '">';
      } else {
        html += '    <input type="text" class="form-control mb-2">';
      }
    }
    html += '  </div>';
    html += '</div>';

    return html;
  }
}

class TextareaQuestion extends Question {
  constructor(text = '', placeholder = '', displayLines = 5, options = {}) {
    super(text, options);
    this.placeholder = placeholder;
    this.displayLines = displayLines;
  }

  renderHTML() {
    var html = '';

    html += '<div class="row mb-3 align-items-center justify-content-center">';
    html += '  <label class="col-sm-2 col-form-label">' + this.text + '</label>';
    html += '  <div class="col-sm-10">';
    html += '    <textarea class="form-control" rows="' + this.displayLines + '" placeholder="' + this.placeholder + '"></textarea>';
    html += '  </div>';
    html += '</div>';

    return html;
  }
}
