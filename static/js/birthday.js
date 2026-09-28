const existingDate = document.getElementById('existing-birthday').value;

function initBirthdayPicker(initialGregorianDate) {
    const options = {
        format: 'YYYY/MM/DD',
        onSelect(unix) {
            const gregorian = new persianDate(unix)
                .toCalendar('gregorian')
                .format('YYYY-MM-DD');
            $('#birthday-hidden').val(gregorian);
        }
    };

    if (initialGregorianDate) {
        const [y, m, d] = initialGregorianDate.split('-').map(Number);
        const dateObj = new Date(y, m - 1, d);
        const unix = dateObj.getTime();  // ✅ تبدیل به timestamp

        options.defaultDate = unix;      // ✅ unix نه string
        options.initialValue = true;

        $('#birthday-hidden').val(initialGregorianDate);

        // نمایش مقدار فارسی در input بعد از init
        const persianFormatted = new persianDate(dateObj.getTime())
    .toCalendar('persian')
    .format('YYYY/MM/DD');
        setTimeout(() => $('#birthday-input').val(persianFormatted), 0);
    }

    $('#birthday-input').persianDatepicker(options);
}

const validDate = existingDate && existingDate !== 'None' ? existingDate : null;
initBirthdayPicker(validDate);

document.getElementById('birthday-input')
$('#birthday-input').length