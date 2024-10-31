from datetime import datetime, timedelta
from django.utils import timezone

class DateFilterMixin:
    def get_date_range(self, period='all'):
        now = timezone.now()
        start_date = None
        end_date = None

        if period == 'custom':
            start_date_str = self.request.GET.get('start_date')
            end_date_str = self.request.GET.get('end_date')
            if start_date_str and end_date_str:
                start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%d'))
                end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%d')).replace(
                    hour=23, minute=59, second=59, microsecond=999999
                )
        elif period == 'today':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif period == 'week':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now
        elif period == 'month':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = now
        elif period == 'year':
            start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = now

        return start_date, end_date