// Déclencher les notifications alertify pour chaque message
                    alertify.set('notifier', 'position', 'top-right');
                    response.messages.forEach(function(message) {
                        if (message.tags.includes('success')) {
                            alertify.success(message.message);
                        } else if (message.tags.includes('error')) {
                            alertify.error(message.message);
                        }
                    });