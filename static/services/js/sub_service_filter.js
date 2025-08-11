(function($) {
    $(document).ready(function() {
        let serviceField = $('#id_service');
        let subServiceField = $('#id_sub_service');

        function updateSubServices() {
            let serviceId = serviceField.val();
            if (!serviceId) {
                subServiceField.html('<option value="">---------</option>');
                return;
            }

            $.ajax({
                url: '/ai/get_sub_services/',
                data: {
                    service_id: serviceId
                },
                success: function(data) {
                    let options = '<option value="">---------</option>';
                    data.forEach(function(item) {
                        options += `<option value="${item.id}">${item.name}</option>`;
                    });
                    subServiceField.html(options);
                },
                error: function() {
                    console.error('Failed to load sub-services.');
                }
            });
        }

        // Initial load
        updateSubServices();

        // Update when service changes
        serviceField.on('change', updateSubServices);

        // Re-bind if Django form reloads via related object popup or inlines
        $(document).on('formset:added', function() {
            serviceField = $('#id_service');
            subServiceField = $('#id_sub_service');
            serviceField.off('change').on('change', updateSubServices);
        });
    });
})(django.jQuery);
