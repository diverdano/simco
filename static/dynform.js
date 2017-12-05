$(document).ready(function() {
    var $aerialTr = $('#id_A').closest('tr').hide();
    var $groundSprayTr = $('#id_B').closest('tr').hide();

    $('#id_application_method').change(function() {
        var selectedValue = $(this).val();

        if(selectedValue  === 'A') {
            $groundSprayTr.hide();
            $aerialTr.show();
        } else if (selectedValue === 'B') {
            $groundSprayTr.show();
            $aerialTr.hide();
        } else {
            $groundSprayTr.hide();
            $aerialTr.hide();
        }
    });
});
