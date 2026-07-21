import logging


class SafeFormatter(logging.Formatter):
    def format(self, record):

        record.uf = getattr(record, "uf", "-")
        record.ano = getattr(record, "ano", "-")
        record.mes = getattr(record, "mes", "-")
        record.total_registros = getattr(record, "total_registros", "-")

        return super().format(record)
