// Main information, chart with area info
let zooFreeArea = document.getElementById('zooFreeArea').innerText;
let zooTotalArea = document.getElementById('zooTotalArea').innerText;

const data = {
  labels: [
    'Free area',
    'Occupied area',
  ],
  datasets: [{
    label: 'My First Dataset',
    data: [zooFreeArea, zooTotalArea - zooFreeArea],
    backgroundColor: [
      '#F4CA16',
      '#359B57'
    ],
    hoverOffset: 4
  }]
};


const config = {
  type: 'pie',
  data,
  options: {}
};

let zooAreaChart = new Chart(document.getElementById('ZooAreaChart'),
    config);


// List of aviaries. Chart with area

let charts = [];

function drawPlacesCharts() {
    $('.av-info').each(function() {
        let amountAnimals = $(this).find('.av-amount-animals').val();
        let needPlace = $(this).find('.living-space').text();
        let Area = $(this).find('.Av-total-area').first().val();
        let AmountPlaces = Math.round(Area / needPlace);
        let freePlaces = AmountPlaces - amountAnimals;

    const data = {
        labels: ['Free places', 'Occupied places'],
        datasets:[
            {
            label: 'Places',
            data: [freePlaces, amountAnimals],
            backgroundColor: ['#318CE7', '#EB4C42'],
            hoverOffset: 4
        }]
    };
    const config = {
        type: 'pie',
        data,
        options: {}
    };
    let places = $(this).find('.ChartInAv-places').first();
    charts.push(new Chart(places, config));
        }
    )
}


function drawAreaCharts() {
$('.av-info').each(function()  {
    let free = $(this).find('.av-free-area').first().text();
    let oc = $(this).find('.av-oc-place').first().text();

    const data = {
        labels: ['Free area', 'Occupied area',],
        datasets: [
            {
                label: 'Area',
                data: [free, oc],
                backgroundColor: ['#F4CA16', '#359B57'],
                hoverOffset: 4
            }]
    };
    const config = {
        type: 'pie',
        data,
        options: {}
    };
    let area = $(this).find('.ChartsInAv').first();
    charts.push(new Chart(area, config));
    })
}


function updateAreaValues(value) {
    let what_this = undefined;
    if (value.attr('class') === 'av-amount-animals') {
        what_this = '.av-amount-animals';
    } else if (value.attr('class') === 'Av-total-area') {
        what_this = '.Av-total-area';
    } else {
        return false;
    }
    let new_value = value.val();
    if (!new_value) {
      return false;
    }

    let parent = value.closest('.av-info');
    let canvas = parent.find('.ChartsInAv').first();
    let chart = charts.filter(f => {
        return $(f.canvas).attr('id') === canvas.attr('id');
    })[0];

    let new_free_area = undefined;
    let new_oc_area = undefined;

    let total_area = parent.find('.Av-total-area').first().val();
    let free_area = parent.find('.av-free-area').first();
    let oc_place = parent.find('.av-oc-place').first();
    let liv_space = parent.find('.living-space').first();

    if (what_this === '.Av-total-area') {
        new_free_area = parseFloat(new_value) - parseFloat(oc_place.text());
        new_oc_area = oc_place.text();

    } else if (what_this === '.av-amount-animals') {
        new_oc_area = parseFloat(new_value) * parseFloat(liv_space.text());
        new_free_area = parseFloat(total_area) - new_oc_area;
        oc_place.text(new_oc_area);
    }
    free_area.text(new_free_area);

    chart.data.datasets[0].data[0] = new_free_area;
    chart.data.datasets[0].data[1] = new_oc_area;
    chart.update();
}


function updatePlacesValues(object) {
    let parent = object.closest('.av-info');
    let amountAnimals = parent.find('.av-amount-animals').val();
    let needPlace = parent.find('.living-space').text();
    let Area = parent.find('.Av-total-area').first().val();
    let AmountPlaces = Math.round(Area / needPlace);
    let occupiedPlaces = amountAnimals * parseFloat(needPlace);
    let freePlaces = AmountPlaces - amountAnimals;


    let canvas = parent.find('.ChartInAv-places');
    let chart = charts.filter(f => {
        return $(f.canvas).attr('id') === canvas.attr('id')
    })[0];

    chart.data.datasets[0].data[0] = freePlaces;
    chart.data.datasets[0].data[1] = amountAnimals;
    chart.update()
}

function setMaxValAnimals(){
    $('.av-amount-animals').each(function () {
        let parent = $(this).closest('.av-info');
        let reqArea = parent.find('.living-space').text();
        let totalArea = parent.find('.Av-total-area').val();
        let maxVal = totalArea / parseFloat(reqArea)
        $(this).attr('max', maxVal);
    })
}

function setMaxValArea() {

        $('.av-info').each(function () {
            let thisAvTotalArea = parseInt($(this).find('.Av-total-area').val())
            let zooFree = getZooFreeArea()
            let maxValue = thisAvTotalArea + zooFree
            let minValue = parseInt($(this).find('.av-oc-place').text())
            $(this).find('.Av-total-area').attr('min', minValue)
            $(this).find('.Av-total-area').attr('max', maxValue);
        });
}

function updMainTable() {
    let newValues = {};

    $('.av-info').each(function () {
         newValues[$(this).find('.animalsType').text()] = $(this).find('.av-amount-animals').val()
    })

    $('.mainTable-row').each(function () {
        let animalValue = $(this).find('.zooAmountAnimals-value');
        animalValue.text(newValues[$(this).find('.zooAmountAnimals-type').text()]);

    })

}

function updateMainInformation() {
    let ocupArea = getOccupiedArea();

    let fullArea = parseFloat($('#zooTotalArea').text());
    let freeArea = Math.round((fullArea - (ocupArea / 1000000)) * 1000) / 1000;
    $('#zooFreeArea').text(freeArea)

    zooAreaChart.data.datasets[0].data[0] = freeArea;
    zooAreaChart.data.datasets[0].data[1] = fullArea - freeArea
    // zooAreaChart.data.datasets[0].data[1] = parseFloat(ocupArea.toString()) / 1000000;
    zooAreaChart.update();
}

function getOccupiedArea() {
    let occupiedArea = 0;
    $('.av-info').each(function () {
        occupiedArea += parseFloat($(this).find('.Av-total-area').val());
    });
    return occupiedArea;
}

function getZooFreeArea() {
    return parseFloat($('#zooFreeArea').text()) * 1000000;
}

function setMaxValNewArviary() {
    $('.newAvTotalArea').attr('max', getZooFreeArea());
}


$().ready(function () {
    drawAreaCharts();
    drawPlacesCharts();
    updateMainInformation();
    setMaxValAnimals();
    setMaxValArea();
    setMaxValNewArviary();
    updMainTable();
});

$('.av-amount-animals').change(function () {
    updateAreaValues($(this));
    updatePlacesValues($(this));
    setMaxValArea();
    updMainTable();
})


$('.Av-total-area').change(function (){


    updateAreaValues($(this));
    updatePlacesValues($(this));
    updateMainInformation();
    setMaxValAnimals();
    setMaxValArea();
    setMaxValNewArviary();

});
