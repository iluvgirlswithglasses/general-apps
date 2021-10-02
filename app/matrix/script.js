
let DEFAULT_FONT_SIZE = 20,
	  DEFAULT_CELL_SIZE = 40,
	  DEFAULT_MATRIX_DIM = 4;

// prefix == s ==> setting
let sFontSize, sCellSize, sRows, sCols;
let eMatrix, eCellStyle, eFontStyle;

/**
 * init
 * */
$(document).ready(() => {
	// 
	eMatrix = $('#matrix');
	eCellStyle = $('.cell-style');
	eFontStyle = $('.cell-font-style');
	// settings
	sFontSize = $('#settings .s-font-size');
	sCellSize = $('#settings .s-cell-size');
	sRows = $('#settings .s-rows');
	sCols = $('#settings .s-cols');
	//
	init();
	setEventListeners();
});

function init() {
	setFont(
		getSetting(sFontSize, DEFAULT_FONT_SIZE)
	);
	setCellSize();
	createMatrix(
		getSetting(sRows, DEFAULT_MATRIX_DIM),
		getSetting(sCols, DEFAULT_MATRIX_DIM)
	);
}

function setEventListeners() {
	// font size listener
	sFontSize.on('change', () => {
		setFont(getSetting(sFontSize, DEFAULT_FONT_SIZE));
	});
	// cell size listeners
	sCellSize.on('change', () => {
		setCellSize();
	});
	// mat dim listeners
	sRows.on('change', () => {
		createMatrix(
			getSetting(sRows, DEFAULT_MATRIX_DIM), 
			getSetting(sCols, DEFAULT_MATRIX_DIM)
		);
	});
	sCols.on('change', () => {
		createMatrix(
			getSetting(sRows, DEFAULT_MATRIX_DIM), 
			getSetting(sCols, DEFAULT_MATRIX_DIM)
		);
	});
}

/**
 * utils
 * */
function createMatrix(rows, cols) {
	//
	eMatrix.html('');
	setCellSize();
	//
	for (let i = 0; i < rows; i++) {
		for (let j = 0; j < cols; j++) {
			let cell = $(`<input class="cell"></input>`);
			eMatrix.append(cell);
		}
	}
}

function setCellSize() {
	let rows = getSetting(sRows, DEFAULT_MATRIX_DIM),
		cols = getSetting(sCols, DEFAULT_MATRIX_DIM),
		cellWidth = getSetting(sCellSize, DEFAULT_CELL_SIZE),
		matrixWidth = cellWidth * cols,
		cellWeight = Math.floor((1/cols) * 100);
	eCellStyle.html(
		`
		#matrix {
			width: ${matrixWidth}px;
		}

		#matrix .cell {
			height: ${cellWidth}px;
			width: ${cellWeight}%;
		};
		`
	);
}

function setFont(s) {
	eFontStyle.html(
		`#matrix .cell {
			font-size: ${s}px;
		};`
	);
}

// 
function getSetting(field, def) {
	let v;
	try {
		v = Math.floor(field.val());
		if (v <= 0) v = def;
	} catch {
		v = def;
	}
	field.val(v);
	return v;
}
