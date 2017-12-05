$(document).ready(function() {
    var $strikeTr = $('#id_strike').closest('input').hide();
    var $couponTr = $('#id_coupon').closest('input').hide();
    var $expiryTr = $('#id_expiry').closest('input').hide();

    $('#id_type').change(function() {
        var selectedValue = $(this).val();

        if(selectedValue  === 'equity') {
            $strikeTr.hide();
            $couponTr.hide();
            $expiryTr.hide();
        } else if (selectedValue === 'option') {
            $strikeTr.show();
            $couponTr.hide();
            $expiryTr.show();
        } else if (selectedValue === 'future') {
            $strikeTr.hide();
            $couponTr.hide();
            $expiryTr.show();
        } else {
            $strikeTr.hide();
            $couponTr.show();
            $expiryTr.show();
        }
    });
});
