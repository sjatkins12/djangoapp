from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from emissions.models import Co2Timestamp

import pandas as pd

# Create your views here.
def get_interpolated_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.resample("30T").mean()
    df["value"] = df["value"].interpolate()

    return df


def get_co2_df_interpollated() -> pd.DataFrame:
    # Get QuerySet and convert to pandas df
    timestamps = Co2Timestamp.objects.all()

    df = pd.DataFrame(list(timestamps.values()))
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.index = df["datetime"]
    del df["datetime"]

    df = get_interpolated_dataset(df)
    return df


def co2_interpollated_view(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponse(status_code=405)

    df = get_co2_df_interpollated()
    return JsonResponse(df.to_json(date_format="iso"), safe=False)


def co2_rate_seasonal_view(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponse(status_code=405)

    def get_season(dt: pd.datetime) -> str:
        """
        Convert a datetime to season
        """
        if dt.dayofyear in range(80, 172):
            return "Spring"
        if dt.dayofyear in range(172, 264):
            return "Summer"
        if dt.dayofyear in range(264, 355):
            return "Fall"
        return "Winter"

    df = get_co2_df_interpollated()
    df = df.groupby(by=get_season).median()

    return JsonResponse(df.to_json(), safe=False)


def co2_rate_day_of_week_view(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponse(status_code=405)

    df = get_co2_df_interpollated()
    df = df.groupby(by=lambda dt: "Weekday" if dt.weekday() < 5 else "Weekend").mean()

    return JsonResponse(df.to_json(), safe=False)
