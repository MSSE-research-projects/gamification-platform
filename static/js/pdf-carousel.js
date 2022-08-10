function PDFCarousel(carousel, feedbacks = {}, options = {}) {
  this.carousel = carousel;
  this.feedbacks = feedbacks;
  this.options = options;

  this.init();
}

PDFCarousel.prototype.init = function () {
  // Loaded via <script> tag, create shortcut to access PDF.js exports.
  this.pdfjsLib = window['pdfjs-dist/build/pdf'];

  // The workerSrc property shall be specified.
  this.pdfjsLib.GlobalWorkerOptions.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.js';

  this.canvas = $(this.carousel).children('.carousel-inner').children('.carousel-item.active').children('canvas')[0];
  this.prevButton = $(this.carousel).children('.carousel-control-prev')[0];
  this.nextButton = $(this.carousel).children('.carousel-control-next')[0];
  this.pageNumber = $(this.carousel).children('.carousel-inner').children('.carousel-item.active').children('.carousel-caption').children('.page-number')[0];
  this.pageCount = $(this.carousel).children('.carousel-inner').children('.carousel-item.active').children('.carousel-caption').children('.page-count')[0];
  this.feedbackTextArea = $(this.carousel).siblings('.feedback-textarea').children('textarea')[0];
  this.ctx = this.canvas.getContext('2d');

  this.pdfDoc = null;
  this.pageNum = 1;
  this.pageRendering = false;
  this.pageNumPending = null;
  this.scale = 0.8;

  this.prevButton.addEventListener('click', this.onPrevPage.bind(this));
  this.nextButton.addEventListener('click', this.onNextPage.bind(this));

  this.renderPage = this.renderPage.bind(this);
  this.renderPDF = this.renderPDF.bind(this);
};

/**
 * Get page info from document, resize canvas accordingly, and render page.
 * @param num Page number.
 */
PDFCarousel.prototype.renderPage = function (num) {
  this.pageRendering = true;
  // Using promise to fetch the page
  this.pdfDoc.getPage(num).then(function (page) {
    var viewport = page.getViewport({ scale: this.scale });
    this.canvas.height = viewport.height;
    this.canvas.width = viewport.width;

    // Render PDF page into canvas context
    var renderContext = {
      canvasContext: this.ctx,
      viewport: viewport
    };
    var renderTask = page.render(renderContext);

    // Wait for rendering to finish
    renderTask.promise.then(function () {
      this.pageRendering = false;
      if (this.pageNumPending !== null) {
        // New page rendering is pending
        this.renderPage(this.pageNumPending);
        this.pageNumPending = null;
      }

      this.feedbackTextArea.value = '';
      if (this.feedbacks[num]) {
        this.feedbackTextArea.value = this.feedbacks[num];
      }

      if (this.options.focus === true) {
        this.feedbackTextArea.focus();
      }
    }.bind(this));
  }.bind(this));

  // Update page counters
  this.pageNumber.textContent = num;
}

/**
 * If another page rendering in progress, waits until the rendering is
 * finised. Otherwise, executes rendering immediately.
 */
PDFCarousel.prototype.queueRenderPage = function (num) {
  if (this.pageRendering) {
    this.pageNumPending = num;
  } else {
    this.renderPage(num);
  }
}

/**
 * Displays previous page.
 */
PDFCarousel.prototype.onPrevPage = function () {
  this.feedbacks[this.pageNum] = this.feedbackTextArea.value;

  if (this.options.onPrevPage) {
    this.options.onPrevPage(this.pageNum, this.feedbackTextArea.value);
  }

  if (this.pageNum <= 1) {
    this.pageNum = this.pdfDoc.numPages;
  } else {
    this.pageNum--;
  }
  this.queueRenderPage(this.pageNum);
}

/**
 * Displays next page.
 */
PDFCarousel.prototype.onNextPage = function () {
  this.feedbacks[this.pageNum] = this.feedbackTextArea.value;

  if (this.options.onNextPage) {
    this.options.onNextPage(this.pageNum, this.feedbackTextArea.value);
  }

  if (this.pageNum >= this.pdfDoc.numPages) {
    this.pageNum = 1;
  } else {
    this.pageNum++;
  }
  this.queueRenderPage(this.pageNum);
}

PDFCarousel.prototype.renderPDF = function (url, onerror) {
  /**
   * Asynchronously downloads PDF.
   */

  this.pdfjsLib.getDocument(url).promise.then(function (pdfDoc_) {
    this.pdfDoc = pdfDoc_;
    this.pageCount.textContent = this.pdfDoc.numPages;

    // Initial/first page rendering
    this.renderPage(this.pageNum);
  }.bind(this)).catch(function (error) {
    onerror();
  }.bind(this));
}