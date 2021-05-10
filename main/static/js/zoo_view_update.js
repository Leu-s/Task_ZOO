function CreateData() {
    let zooId = parseInt($('.zoo-mainInfo').attr('id'));
    let aviaries = {};

    $('.av-info').each(function () {
        let animalType = $(this).find('.animalsType').text();
        let amountAnimals =$(this).find('.av-amount-animals').val();
        let totalArea = $(this).find('.Av-total-area').val();

        aviaries[animalType] = {
            'amountAnimals': amountAnimals,
            'totalArea': totalArea
        };
    });

    return {
        zooId: zooId,
        'aviaries': aviaries,
    };
}


$('#SaveBtn').click(function () {
    $.ajax(
        {
            method: "POST",
            url: $(this).attr('value'),
            data: {
                'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'newData': JSON.stringify(CreateData())
            },
            dataType: 'json',
            success: function (data) {
                if (data['allSaved']) {
                    alert('Information has been successfully updated.');
                } else {
                    alert('Some of the new information was not saved, check the correctness of the data.')
                }

                console.log(data);
            },
            error: function (data) {
                alert('An unknown error has occurred');
                console.log(data);
            }
        }
    )
})
