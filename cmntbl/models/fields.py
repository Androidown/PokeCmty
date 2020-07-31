#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.db import models


class PositiveTinyIntegerField(models.PositiveIntegerField):
    description = "Unsigned Tiny Integer."

    def db_type(self, connection):
        return "TINYINT UNSIGNED"

    def rel_db_type(self, connection):
        return "TINYINT UNSIGNED"
