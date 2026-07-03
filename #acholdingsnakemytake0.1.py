#!/usr/bin/env python3
"""
ac's snake my take 0.1
Nokia 3310 style snake game — 60 FPS, pure pygame, single file.
files = off · Lorenzo Brooks sprites (GitHub/YouTube) · base64 RAM embed
"""

import array
import base64
import io
import pygame
import sys
import random

FILES = False  # files = off — embedded base64 assets only, no disk reads
ASSET_SOURCE = "itspyguru/Python-Games · Lorenzo Brooks (GitHub/YouTube)"

# ── github/youtube snake sprites · base64 embed · files = off ──
ASSET_B64 = {
    "food_1": (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA9klEQVQ4EcVQOw7CMAx1EWfhAgyc"
        "gAGJK3RFYkOcAFaOgASH4DOhql0ZOAITBwnvuXGblAaxYcmxnef37EQkbS4NtcigTaPMuavWP4kY"
        "k81u5kQjc++G90bbQCeNcT4rkaVWItVaOSbkb2MdE8hwnT14wopKhGK0V77TVRhhvSIEQnMlGkdl"
        "/QQQHVjqzNEYiQxDJkFDiyMm5jW6RVjd7nKYTpTtF+1QUZ78JJsYxk2AodXmxCILAN9EKEg8FLBP"
        "VKV9rPdTFQmQcYGfE1TeE4c139D9RAL6vj4RkrtbdgU+GjhuDg/IzXRiKXP8UIDqQZ7q/+P9GxZd"
        "brcSPDYpAAAAAElFTkSuQmCC"
    ),
    "food_2": (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABBUlEQVQ4EbVSu3FCMRDcxzhx4Bbg"
        "xaQQugEaIfRgoAAawNhNuAt3gCMaeJEDMmacEJ139SSNBHpvTMDN6HN3u6s7SUBulrvR64pjECGA"
        "TQjjEDgQFLPxh0OFWEJBJlApc3wHZoQa7WnU+o8vGSdz0gpi4qsGpqjw3MRQ5+YhzXyzBrUhO9TA"
        "uTEMKaQ4rZ3dtn+ShBsX99HPSrJq3/a8BQ2ZBLX3wgm0UBYvXUDWW7EMcyvJkaS7cWkfKfVlS+wi"
        "4Q2vkL/FwsUkTCvxIoclXJUt0WIL2SsEiRX4GWifXNWG7D8nO6Cf4oldJwdw8SMp+YsT5thg7XsP"
        "hFtW++l4ultE7o/9AxtVZCl2VEmnAAAAAElFTkSuQmCC"
    ),
    "food_3": (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA2ElEQVQ4EdVSuQ0CMAx0ED2r8EiM"
        "QAcFomIBZqKghQYxCBKwADOwgvE5ymdHQIulJH7uLo4VomJcXILPsCrXdYcpO4tQ3W+BaLQkWpA4"
        "X2xQ15+rGK2P8XzVxV986YLlZsYpeLu6Er0e9Rm89/iw82/KM6jhjjyX6lhbYiviOhCydqCCIF4r"
        "aYnDROPMa4YopUIGDmSIJJPYdmcF6FTfCKKJbd0JXB7pOn+CbOt2iHgbBuVahdz24EW7mc00/gEM"
        "NC0Bpn/RcPI0m2wMWISyne/qfsJn7J85bzclQpfa27S0AAAAAElFTkSuQmCC"
    ),
    "head_up": (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJN"
        "AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABrVBMVEUAAABjx01VqkJXr0Re"
        "vElfyk1ZwEmJuVKMv01gr02JxFFOsERMrENMzCNH0yB3t0Fcsi5EizpCiDkzaS02aylCgzM5dzU9"
        "ei89eS5TpkBOnj1Roz9Xr0RWzEtiyE1hxkxOu0ejwVVarktvs02Mv01jsE2SyFJNskNKq0FM2hw+"
        "3RV+tj9MqyRAhTZAgzY3cC43cS41aSc6djE4dTE+fTI9eS4+fDE+fTM9eC08dyw+fjNBiDxBhzw8"
        "eCw7dStEijVKlDlBgzJLmTt6xk5hqEJLmjtNmTt5vEpqyE1qvkuUy1Fns0aCwUyHyU9Xsklgsktz"
        "wU1sxEyHwkyGxk5mwUxwuktksk1YskhUn0tbpluIzFl/vVhZn1tdr0xTsElQsDtZo1XC2c+Y0o+U"
        "zY7B2M9dq1hZuj9pukdQnkQsVUs4bUA3bUAqUEpJkkJ2vkZTgjhgjT1GhDNEkj9gnUVEfzJCfjdS"
        "fzcgRB9WoT55v0trvUllwEpbnD0fQx9SqUNvxE14v0tes0VvxU5xt0pGkT1GlEBXpUVoqkdImENH"
        "kz8yaC1FjztEjDozajH///+NCsksAAAAP3RSTlMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJufn"
        "JgqlpQpO9vZOgYGAgICAgICAgHV1I93dgBarqxYVp+bmDBxY8+brAAAACXBIWXMAAA7DAAAOwwHH"
        "b6hkAAAAAWJLR0SOggWzbwAAAAd0SU1FB+YFFBItEtdjQT4AAAAldEVYdGRhdGU6Y3JlYXRlADIw"
        "MjItMDUtMjBUMTg6NDU6MTArMDA6MDCVLDhMAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIyLTA1LTIw"
        "VDE4OjQ1OjEwKzAwOjAw5HGA8AAAAMhJREFUKFNjwA7EwQDKAQJxCVs7O1sJuIi4hKWVjbWVJUyN"
        "uISFeW9Pd5eZKVSNqJhJZ0d7W2uLiZgoWEDE0Li5qbGhvs7IUAQsIGxQW1NZXVVZUa4vDBYQ0isr"
        "LSkuKizI1xUECwjo5OXmZGdlZqRr84MF+LTSUlOSkxIT4jV5wQI8GnGxMdFRkRHh6txgAS61sNCQ"
        "4KDAAH9VTrAAh4qyn6+Pt5enkiI7WIBNQd7D3c3VxVlOlhUswMIsI+3k6GAvJcnEyMAAAKZYKq4l"
        "SrIKAAAAAElFTkSuQmCC"
    ),
    "head_down": (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJN"
        "AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABrVBMVEUAAABjx01VqkJXr0Re"
        "vElfyk1ZwEmJuVKMv01gr02JxFFOsERMrENMzCNH0yB3t0Fcsi5EizpCiDkzaS02aylCgzM5dzU9"
        "ei89eS5TpkBOnj1Roz9Xr0RWzEtiyE1hxkxOu0ejwVVarktvs02Mv01jsE2SyFJNskNKq0FM2hw+"
        "3RV+tj9MqyRAhTZAgzY3cC43cS41aSc6djE4dTE+fTI9eS4+fDE+fTM9eC08dyw+fjNBiDxBhzw8"
        "eCw7dStEijVKlDlBgzJLmTt6xk5hqEJLmjtNmTt5vEpqyE1qvkuUy1Fns0aCwUyHyU9Xsklgsktz"
        "wU1sxEyHwkyGxk5mwUxwuktksk1YskhUn0tbpluIzFl/vVhZn1tdr0xTsElQsDtZo1XC2c+Y0o+U"
        "zY7B2M9dq1hZuj9pukdQnkQsVUs4bUA3bUAqUEpJkkJ2vkZTgjhgjT1GhDNEkj9gnUVEfzJCfjdS"
        "fzcgRB9WoT55v0trvUllwEpbnD0fQx9SqUNvxE14v0tes0VvxU5xt0pGkT1GlEBXpUVoqkdImENH"
        "kz8yaC1FjztEjDozajH///+NCsksAAAAP3RSTlMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJufn"
        "JgqlpQpO9vZOgYGAgICAgICAgHV1I93dgBarqxYVp+bmDBxY8+brAAAAAWJLR0SOggWzbwAAAAd0"
        "SU1FB+YFFBItEtdjQT4AAADKSURBVBjTY2BgYGSSlLJ3cHSSlmFmYQABVlk5ZxdXN3cPeQU2sAC7"
        "opKnl7ePr5+yCgdYgFPVPyAwKDgkNEyNCyzArR4eERkVHRMbp8EDFuDVjE9ITEpOSU3T4gML8Gun"
        "Z2RmZefk5ukIgAUEdfMLCouKS0rL9ITAAsL65RWVVdWVNbUGwmABEUOjuvqGxqZmY0MRsIComElL"
        "a1t7R6eJmChYQFzC1Kyru6fX3EJCnAEiIm5pZW1jZQnjg9TY2tnZIvggNSDAgBUAALYsKq4DFlal"
        "AAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIyLTA1LTIwVDE4OjQ1OjEwKzAwOjAwlSw4TAAAACV0RVh0"
        "ZGF0ZTptb2RpZnkAMjAyMi0wNS0yMFQxODo0NToxMCswMDowMORxgPAAAAAASUVORK5CYII="
    ),
    "head_left": (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJN"
        "AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABrVBMVEUAAABjx01VqkJXr0Re"
        "vElfyk1ZwEmJuVKMv01gr02JxFFOsERMrENMzCNH0yB3t0Fcsi5EizpCiDkzaS02aylCgzM5dzU9"
        "ei89eS5TpkBOnj1Roz9Xr0RWzEtiyE1hxkxOu0ejwVVarktvs02Mv01jsE2SyFJNskNKq0FM2hw+"
        "3RV+tj9MqyRAhTZAgzY3cC43cS41aSc6djE4dTE+fTI9eS4+fDE+fTM9eC08dyw+fjNBiDxBhzw8"
        "eCw7dStEijVKlDlBgzJLmTt6xk5hqEJLmjtNmTt5vEpqyE1qvkuUy1Fns0aCwUyHyU9Xsklgsktz"
        "wU1sxEyHwkyGxk5mwUxwuktksk1YskhUn0tbpluIzFl/vVhZn1tdr0xTsElQsDtZo1XC2c+Y0o+U"
        "zY7B2M9dq1hZuj9pukdQnkQsVUs4bUA3bUAqUEpJkkJ2vkZTgjhgjT1GhDNEkj9gnUVEfzJCfjdS"
        "fzcgRB9WoT55v0trvUllwEpbnD0fQx9SqUNvxE14v0tes0VvxU5xt0pGkT1GlEBXpUVoqkdImENH"
        "kz8yaC1FjztEjDozajH///+NCsksAAAAP3RSTlMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJufn"
        "JgqlpQpO9vZOgYGAgICAgICAgHV1I93dgBarqxYVp+bmDBxY8+brAAAACXBIWXMAAA7DAAAOwwHH"
        "b6hkAAAAAWJLR0SOggWzbwAAAAd0SU1FB+YFFBItEtdjQT4AAAAldEVYdGRhdGU6Y3JlYXRlADIw"
        "MjItMDUtMjBUMTg6NDU6MTArMDA6MDCVLDhMAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIyLTA1LTIw"
        "VDE4OjQ1OjEwKzAwOjAw5HGA8AAAALhJREFUKFNjIA6Ii4oIC/LzcnOyszKC+RJihvq62prqqoqy"
        "TCC+uKmJUXl+eny4v5KcJEje0qylrqIgIyEiwNNZCihga9XVWl9ZmJkYGejlYg8UsLPubmuoKspK"
        "igrydnUACdj0tDdWF2cnRwf7uDmCtfR2NFWW5KTEhPi6O4ENNe9srinNTY0N9fOQBjvDwsS4tiwv"
        "LS5MWV4G5jADPR0tDTUVBWaQANjpQgJ8PFwcbCxgATyAgQEAb/8qrlx+/SUAAAAASUVORK5CYII="
    ),
    "head_right": (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJN"
        "AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABrVBMVEUAAABjx01VqkJXr0Re"
        "vElfyk1ZwEmJuVKMv01gr02JxFFOsERMrENMzCNH0yB3t0Fcsi5EizpCiDkzaS02aylCgzM5dzU9"
        "ei89eS5TpkBOnj1Roz9Xr0RWzEtiyE1hxkxOu0ejwVVarktvs02Mv01jsE2SyFJNskNKq0FM2hw+"
        "3RV+tj9MqyRAhTZAgzY3cC43cS41aSc6djE4dTE+fTI9eS4+fDE+fTM9eC08dyw+fjNBiDxBhzw8"
        "eCw7dStEijVKlDlBgzJLmTt6xk5hqEJLmjtNmTt5vEpqyE1qvkuUy1Fns0aCwUyHyU9Xsklgsktz"
        "wU1sxEyHwkyGxk5mwUxwuktksk1YskhUn0tbpluIzFl/vVhZn1tdr0xTsElQsDtZo1XC2c+Y0o+U"
        "zY7B2M9dq1hZuj9pukdQnkQsVUs4bUA3bUAqUEpJkkJ2vkZTgjhgjT1GhDNEkj9gnUVEfzJCfjdS"
        "fzcgRB9WoT55v0trvUllwEpbnD0fQx9SqUNvxE14v0tes0VvxU5xt0pGkT1GlEBXpUVoqkdImENH"
        "kz8yaC1FjztEjDozajH///+NCsksAAAAP3RSTlMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJufn"
        "JgqlpQpO9vZOgYGAgICAgICAgHV1I93dgBarqxYVp+bmDBxY8+brAAAACXBIWXMAAA7DAAAOwwHH"
        "b6hkAAAAAWJLR0SOggWzbwAAAAd0SU1FB+YFFBItEtdjQT4AAAAldEVYdGRhdGU6Y3JlYXRlADIw"
        "MjItMDUtMjBUMTg6NDU6MTArMDA6MDCVLDhMAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIyLTA1LTIw"
        "VDE4OjQ1OjEwKzAwOjAw5HGA8AAAALdJREFUKFNjIAxY2Di4ePgEhIRFRMXBAswKKmoaWjp6BoZi"
        "EmARGXnlsLi0vLJaYxMLsIi0h19obGpuaU1zp7klSMTJ3TckJiWnpLKpo9fKFijg6OYTHJ2cXVzd"
        "2N5jYwcUcHD1DopKyiqqamjrtgYJ2Lt4BUYmZhZW1rd2gbVIOXsGRCRkFFTUtZiBDZWUU/IPj0/P"
        "LzcyMRUH8hmYZBVV1TW1dfVhDmNkZefk5uUXhDudAGBgAADshSqutgcz7wAAAABJRU5ErkJggg=="
    ),
    "body_h0": (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABi0lEQVRYCc2XvY0CMRCFbxElkJCc"
        "iEiRyAhOVLBFIHQhDVAADRAiRBFUcLqADImUCJGQUAMHMv6M9mmNFyRuIBnmx8N7z7Nek31EPl/j"
        "zl8kVSn8M+q6uu/d0dl5b5mVLayVBf8zVtcfG65yx3y73BdS7fyz4JOHaSF5cWA+azWuKd+XOhR5"
        "HwVgDkIsDGEEcxQhTj0W5uTxyc/9F3MFMpjDDIQp5tSlrPalnv72CujzDjL2DsQxJuSZCXzqNU4e"
        "a65AOAeUOQxAiqUOvz9du6+xeupi1lyB7HQYuJMPJoo0tYc838xMSgntZ69A1XNAlVEf5jojMWVQ"
        "wlyBOshhBAOQE49Z1sfWhRnJrx2op5+5AuFdEJD6GwwIsYqcuFr2VuP42sdcgdsMjPzNxUNVpDBg"
        "rzk3lLGu07z65gqEk5CpVwYwx/5ONqW3W/L6diWuzJk5ewVSJyF7nWIOU7XaX5WwV0D3TKf8WeZV"
        "lXgfBWBeay7uTrkye9TXmTBXINwJX80cpfhPiBLmCpwB13vIBsro5IkAAAAASUVORK5CYII="
    ),
    "body_h1": (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABfElEQVRYCc3XPUpDQRQF4LzgEmxs"
        "xMpWsLOQrCCLELF0Ay7ADViKuIisQCzsBFsrsbFxDWoc/ZoDw4uomXlFbu7PzJxz7n0Dbzg823uf"
        "LJ/b84fh067rOb6bl3On6zqwds6GxNvL0Reiret/VQLzx8VzObofBWYX9wURJfh/NRvJfHe+3YkC"
        "kOgJ5jen+wXhbDL51VtSY142X/40n4FBz0+eXgsoSkCYdmwm3Cu5jtLilzub5W97BSDW8zEl1JmV"
        "ZJYKZp4CbHsFTKmeUABCNpmJpx1jnPu0V8AMYKLHNSXUsRjV1qWy6inVXgEzABlmNUbyaa23Tp6S"
        "8uL9KOAm9F5DyELKT1vrcdbxc7/2M+At0LtazzBQx68pJ5+Mxdl+FIAIQ0qI5xSLs8lUfcbVs+0V"
        "WPUeWJURZqx1fJbS7RWAiBJ8yCE1E+Jjvc37gW//6ff3Rz8KQEYJTMWTsTyF1LEUw5wvf3WwKF9g"
        "/SkAoRuS/1NLGcwxzn2aK/ABpvDOrWRGSMMAAAAASUVORK5CYII="
    ),
    "body_v0": (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABiklEQVRYCc3WvU0DQRCG4TuLEkhI"
        "EBEpEhkBcgUuAiGHNEABNECIEEW4AkRAhkRKhJyQUAM/Xvyc5IHTHhJizoHHs/vder53d0fXnt7P"
        "3pvPz9NiuQrN/my3RF9Xe9vl5/z5tcQ+HX2Mnp/s3LRxbpVPfhr8z7GuqhoJRSEgFyM54/S3Z4dl"
        "CMnro0X573QCWypVUY1EdMqhGOet3xfHQ0CFQ0k43fPZ15MIWCdGe++5Zn370gl0tyBWLD8+Pyh9"
        "Qh73mKPp5QPJRqSniyTSCXS3YKPsP0g4t1R0jtj4CdxdPJZzEvuDzsYJx7XbgIg4fgIqjTE6d8qn"
        "zbJIkUAmPi9PJ1DtAyqt9QO6jsS6L0QCyNCnExjcB+Kp52Bo5BwReTqB6hmIe88xJ3KRM7kY9XTp"
        "BHrPwG+dcypGx/F20I2PAOdDT32fMw5r8+kEvt2Ct5eT8gak13MydE/ponPj1vPumU6guwU15xxx"
        "EAkZp+ub55w+nUDr1KtItGfRkXGdTB51cZ3o3Hw6gQ8z0Ko2MNBcyAAAAABJRU5ErkJggg=="
    ),
    "body_v1": (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABh0lEQVRYCc2WMU7DQBBFbYsj0NAg"
        "KlqkdBTIJ/AhIpSSC3AAXyBlhDhEToAo6JDSpopoaDgDQR54q/ij0TpCYjbNaLx/d+e/WTtbV87v"
        "832+H4YWuw9HMX68Xb/Zg8vu3OLq4tSizlddM17m/7OaLW9fOnNM5e3y1YZwhI6IE3JiTs/4w/Xa"
        "9g4ncELlU6M6x5E3Hz06nKOPJ6C911NLpRpxxJnReTnnrBdPQB2kvPuuESdUTEw6+U6oXnvOfGI8"
        "Ad73p7uZFaW9pNfqDAd/jfEEjnUAESVHzniu9+xbPgHtfTr9P28JznF0bCyHAE7ooTqZ+pYoMV1H"
        "83II4BwH5FpxLodU029yUhsPJ1Df3F/ZTUgdQ0JtqI5xT//cb9KtC+1hLIcAVdFD/U/AoUeA+ejI"
        "iR6JcAK/7oR8D3IkvHEcE9G1VWVnTUmEE0gnlLshldNLHHAmeI5Ox3nu6Zqzx7TnoC2HAJVDwnPA"
        "GUFPhAR5jhgkyiOAgxwJdcj3AXIQUR3rE8MJfAEmH8Mdc2EmigAAAABJRU5ErkJggg=="
    ),
    "body_corner_l": (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABlklEQVRYCdXWsU0DQRCFYZ/lEkhI"
        "EBEpEhkBcgUuAiGHNEABboAQIYpwBYiADMkpESIhoQZAXvEh3zNnm2gPB56b2dnVvH93564ZfP8+"
        "3s4/PS/t9OW9uDeHe8Xyi/PL3/P8tUSPJgfFmje+fmrFTb09nTfL56FALdtQrtIshKKMd/nbSJhn"
        "3foELh4nrb1XIZuKMs5PS6F4ngnx/0NAxWnvL09aoW1nKUn0j4A9b8lacewtJbv2h5UlyiNy1QmM"
        "VJbKU6k8ezydiGy2lJonG7nqBBp9AIFUrlKV23uK5BvvsjlPXn8JqDAtUhlPv4sMEshWJ/BzC1JB"
        "l5/KEMnTLm6drnnVCax9D2SlFKSlkPLh/l35wjm7Ot74drW+s1CfgD5AIWUqFU8rL+MPs0WLBEL6"
        "hnzr94+ACilUqXhaeRnflUR1AiMKupQat5c6WCrmyxsPBuU2IDGcLUpKfoVXJ7D2NqSAUgRSoXHx"
        "rjz9QR6rX/SPgAqRyPub43xE/kqiPgEKdMQuBanQrZGPWOZZn3Ur+NUJfAEm3ehXelR9xAAAAABJ"
        "RU5ErkJggg=="
    ),
    "body_corner_r": (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABjUlEQVRYCc3XMUpDQRAGYF/IEWxs"
        "xMpWsLMQT5BDiFjmAh7AC1iKeAhPIBZ2gq2V2Nh4BpVs8j3MwLAiyCRF/jezs8v8/8zu2zdsrX5n"
        "j7Mvzwt8uXtr5v38sOH560dD/v3ZbrOzv+u97bV5bPGTndth8TzhqMIBc8wk8lfm5sO4Lr/16xU4"
        "vjhYq73M1FzGGRPjsSfER794WK7AVCaROQbGoTj2ydVTe8zixWVYrsDw+X7aegCTmGmvhva3nukp"
        "EderV+C350BUJtqYxx7JlKFEuQJTmWOEgcz5MzQ/mzf2yGy5gnjr1SugFmOmq7eeDGHMnB/aRdbj"
        "7ylZr8DIbL58f8t89HOsUK0zxiG8a9YrgJFaZcxRcZOJJ2isvfgM9Vy5At0bkVo/XD63O1y8P2DY"
        "U4CyMa5cgfQk/G/mlKtXQCZ2gy7nV3PjlDEeUXf34vTE5igQmWOWMY/dnDEXF8f5yxVoexvbnxhP"
        "OmMyx4g/q3lPwc1TQNdjBiNzjPl1NZtC4uI6N0d3m/F1/A03ss63/S4AqQAAAABJRU5ErkJggg=="
    ),
    "tail": (
        "iVBORw0KGgoAAAANSUhEUgAAADQAAAAiCAYAAAAQ9/ptAAACWElEQVRYCe1XMU4DMRBMEE+gh44H"
        "UNHwA5RHIOq8hRrxCMQPaKh4AB30/AE0J421tzf27V7ukiBhKYm9nh3PeK2Lb7VqtLu32x98GpDe"
        "VAbbSwwOInpOglwh2NP1y3ppU2NC1jWAFwaxNayN27xojs2v9S0vMDXuWSvkF/IiamLnjM9uaE5x"
        "U7gWMWSPA6q0z0pJQxDw8fxVNgj9jCiFVbGywEgno0caAv/l5nz1eHHWfdDPNFshciB/F1NRPYMn"
        "Fxe1FYIYmrJiEVeNHJhTPBEO8pJL8QDjuaoVIuGUX7+I56BIH59jLA1hN163V4Uffb9DZVJ0KLjF"
        "Q4xIH4RaPB7cM+QX4TG7eXgvBj3GE6qx4lE4H/NrKR6P6RnyhH6cqZLPteMleaQhHLH7z+9yzDBG"
        "lbLtEDzFEEuHx2zNDEqO3SVWGeTcoXg6QxkR2HU05lhTjEXM7IPHavvv//kd4PGKGAE2g49w1jDl"
        "oVADqDjEjd0GVN4+YoO7XGtRu8tRQzYH3NG8lo7WXLhCVtjSolqCx+bChsaIjmX+dEyIrQywx1wd"
        "6GtWyJtBgoohrhqw9t42dstQHNlYtUIUjn99NFyH0LIVwnWpcGw6ikW/5FPO7ywU8OqOfsQUN8RW"
        "yPJEOIDPtsGRo5Aa0VJCautl4z1DNINd5eURhOhzp4mJLNTiieRPwfQMeQIeM/vG6jFq7E0rHo9R"
        "PFNiTUOekFXy8ex4Lh61rjSEI1Z7yVMktdhcPDV+FS+GeAQiL2fEKkLO7cqjuCOxzlBGBB8WzLGL"
        "MBYx0+KxnNn+Lwlb3OLi+lctAAAAAElFTkSuQmCC"
    ),
}

# total embedded: 8140 bytes raw

# ── init ──────────────────────────────────────────────────────────────
pygame.init()

# ── nokia 3310 lcd palette ───────────────────────────────────────────
LCD_BG      = (67, 107, 63)       # dark green lcd background
LCD_PIXEL   = (106, 153, 78)      # slightly lighter green (grid lines)
LCD_ON      = (162, 193, 124)     # bright green — "pixel on"
LCD_TEXT    = (205, 235, 165)     # high-contrast ui text
LCD_TEXT_DIM = (155, 190, 120)    # readable inactive menu text
LCD_DARK    = (56, 90, 52)        # darker green for dead zones
LCD_BORDER  = (45, 75, 42)        # bezel green
BEZEL       = (30, 30, 30)        # phone body dark grey
BEZEL_LIGHT = (55, 55, 55)        # phone body highlight

# ── grid / cell sizing ────────────────────────────────────────────────
CELL       = 16
COLS       = 21
ROWS       = 19
GRID_W     = CELL * COLS   # 336
GRID_H     = CELL * ROWS   # 304
PADDING    = 28
BEZEL_THICK = 14
WIN_W      = GRID_W + PADDING * 2 + BEZEL_THICK * 2
WIN_H      = GRID_H + PADDING * 2 + BEZEL_THICK * 2 + 40  # extra for score bar

# ── nokia-style pixel font (hand-crafted 5x7 bitmaps) ────────────────
FONT_DATA = {
    '0': [0x7C,0xC6,0xCE,0xD6,0xE6,0xC6,0x7C],
    '1': [0x18,0x38,0x78,0x18,0x18,0x18,0x7E],
    '2': [0x7C,0xC6,0x06,0x1C,0x30,0x60,0xFE],
    '3': [0x7C,0xC6,0x06,0x3C,0x06,0xC6,0x7C],
    '4': [0x1C,0x3C,0x6C,0xCC,0xFE,0x0C,0x0C],
    '5': [0xFE,0xC0,0xFC,0x06,0x06,0xC6,0x7C],
    '6': [0x3C,0x60,0xC0,0xFC,0xC6,0xC6,0x7C],
    '7': [0xFE,0xC6,0x0C,0x18,0x30,0x30,0x30],
    '8': [0x7C,0xC6,0xC6,0x7C,0xC6,0xC6,0x7C],
    '9': [0x7C,0xC6,0xC6,0x7E,0x06,0x0C,0x78],
    'A': [0x18,0x3C,0x66,0x7E,0x66,0x66,0x66],
    'B': [0xFC,0x66,0x66,0x7C,0x66,0x66,0xFC],
    'C': [0x3C,0x66,0xC0,0xC0,0xC0,0x66,0x3C],
    'D': [0xF8,0x6C,0x66,0x66,0x66,0x6C,0xF8],
    'E': [0xFE,0x62,0x68,0x78,0x68,0x62,0xFE],
    'F': [0xFE,0x62,0x68,0x78,0x68,0x60,0xF0],
    'G': [0x3C,0x66,0xC0,0xC0,0xCE,0x66,0x3E],
    'H': [0xC6,0xC6,0xC6,0xFE,0xC6,0xC6,0xC6],
    'I': [0x7E,0x18,0x18,0x18,0x18,0x18,0x7E],
    'J': [0x1E,0x06,0x06,0x06,0xC6,0xC6,0x7C],
    'K': [0xC6,0xCC,0xD8,0xF0,0xD8,0xCC,0xC6],
    'L': [0xC0,0xC0,0xC0,0xC0,0xC0,0xC0,0xFE],
    'M': [0xC6,0xEE,0xFE,0xD6,0xC6,0xC6,0xC6],
    'N': [0xC6,0xE6,0xF6,0xDE,0xCE,0xC6,0xC6],
    'O': [0x7C,0xC6,0xC6,0xC6,0xC6,0xC6,0x7C],
    'P': [0xFC,0x66,0x66,0x7C,0x60,0x60,0xF0],
    'Q': [0x7C,0xC6,0xC6,0xC6,0xD6,0xDE,0x7C],
    'R': [0xFC,0x66,0x66,0x7C,0x6C,0x66,0xE6],
    'S': [0x7C,0xC6,0xC0,0x7C,0x06,0xC6,0x7C],
    'T': [0xFE,0x92,0x10,0x10,0x10,0x10,0x10],
    'U': [0xC6,0xC6,0xC6,0xC6,0xC6,0xC6,0x7C],
    'V': [0xC6,0xC6,0xC6,0xC6,0x6C,0x38,0x10],
    'W': [0xC6,0xC6,0xC6,0xD6,0xFE,0xEE,0xC6],
    'X': [0xC6,0xC6,0x6C,0x38,0x6C,0xC6,0xC6],
    'Y': [0xC6,0xC6,0x6C,0x38,0x18,0x18,0x18],
    'Z': [0xFE,0x86,0x0C,0x18,0x30,0x62,0xFE],
    ' ': [0x00,0x00,0x00,0x00,0x00,0x00,0x00],
    ':': [0x00,0x18,0x18,0x00,0x18,0x18,0x00],
    '.': [0x00,0x00,0x00,0x00,0x00,0x18,0x18],
    '-': [0x00,0x00,0x00,0x7E,0x00,0x00,0x00],
    '!': [0x18,0x18,0x18,0x18,0x18,0x00,0x18],
    '>': [0x60,0x30,0x18,0x0C,0x18,0x30,0x60],
    '<': [0x06,0x0C,0x18,0x30,0x18,0x0C,0x06],
    '/': [0x06,0x0C,0x18,0x30,0x60,0xC0,0x80],
    "'": [0x18,0x18,0x30,0x00,0x00,0x00,0x00],
    's': [0x00,0x00,0x7C,0xC6,0xC0,0x7C,0x06],
    'c': [0x00,0x00,0x3C,0x66,0xC0,0x66,0x3C],
    't': [0x10,0x30,0x7E,0x30,0x30,0x36,0x1C],
    'k': [0xC0,0xC0,0xCC,0xD8,0xF0,0xD8,0xCC],
    'e': [0x00,0x00,0x7C,0xC6,0xFE,0xC0,0x7C],
    'a': [0x00,0x00,0x38,0x0C,0x7C,0xCC,0x7C],
    'p': [0x00,0x00,0xF8,0x6C,0x66,0x6C,0xF0],
    'h': [0xC0,0xC0,0xF8,0xCC,0xCC,0xCC,0xCC],
    'r': [0x00,0x00,0xDC,0x76,0x60,0x60,0xF0],
    'n': [0x00,0x00,0xF8,0xCC,0xCC,0xCC,0xCC],
    'o': [0x00,0x00,0x78,0xCC,0xCC,0xCC,0x78],
    'y': [0x00,0x00,0xCC,0xCC,0x7C,0x0C,0xF8],
    'w': [0x00,0x00,0xC6,0xC6,0xD6,0xFE,0x6C],
    'i': [0x00,0x18,0x38,0x18,0x18,0x18,0x3C],
    'l': [0x60,0x60,0x60,0x60,0x60,0x60,0x3C],
    'd': [0x06,0x06,0x3E,0x66,0x66,0x66,0x3E],
    'v': [0x00,0x00,0xC6,0xC6,0x6C,0x38,0x10],
    'm': [0x00,0x00,0xEC,0xFE,0xD6,0xD6,0xD6],
    'u': [0x00,0x00,0xCC,0xCC,0xCC,0xCC,0x78],
    'f': [0x1C,0x30,0x7C,0x30,0x30,0x30,0x30],
    'g': [0x00,0x00,0x7C,0xC6,0x7E,0x06,0x7C],
    'b': [0xC0,0xC0,0xF8,0xCC,0xCC,0xCC,0xF8],
    'x': [0x00,0x00,0xCC,0x6C,0x38,0x6C,0xCC],
    'z': [0x00,0x00,0xFC,0x98,0x30,0x64,0xFC],
    'j': [0x0C,0x0C,0x3C,0x0C,0x0C,0xCC,0x78],
    'q': [0x00,0x00,0x78,0xCC,0xCC,0x7E,0x06],
}

PIXEL_SCALE = 2
FONT_SCALE_UI = 3   # menus / overlays — bigger + easier to read
FONT_SCALE_HUD = 2  # compact score bar below lcd
CHAR_W = 5 * PIXEL_SCALE
CHAR_H = 7 * PIXEL_SCALE
CHAR_GAP = 1 * PIXEL_SCALE


def _char_metrics(scale):
    return 5 * scale, 7 * scale, scale


def draw_char(surface, ch, x, y, color=LCD_TEXT, scale=FONT_SCALE_UI, shadow=True):
    """Draw a single character using bitmap font data."""
    ch_up = ch.upper()
    if ch_up not in FONT_DATA:
        if ch in FONT_DATA:
            ch_up = ch
        else:
            cw, _, gap = _char_metrics(scale)
            return cw + gap
    data = FONT_DATA[ch_up]
    cw, ch_h, gap = _char_metrics(scale)

    def _blit_glyph(ox, oy, draw_color):
        for row_i in range(7):
            row = data[row_i]
            for col_i in range(5):
                if row & (1 << (7 - col_i)):
                    px = x + col_i * scale + ox
                    py = y + row_i * scale + oy
                    pygame.draw.rect(surface, draw_color, (px, py, scale, scale))

    if shadow and scale >= FONT_SCALE_UI and color not in (LCD_DARK, LCD_BG):
        _blit_glyph(scale // 2, scale // 2, LCD_DARK)
    _blit_glyph(0, 0, color)
    return cw + gap


def draw_text(surface, text, x, y, color=LCD_TEXT, scale=FONT_SCALE_UI):
    """Draw a string of characters, returns width used."""
    cx = x
    for ch in text:
        w = draw_char(surface, ch, cx, y, color, scale)
        cx += w
    return cx - x


def text_width(text, scale=FONT_SCALE_UI):
    cw, _, gap = _char_metrics(scale)
    return len(text) * (cw + gap) - gap


def draw_text_centered(surface, text, cx, y, color=LCD_TEXT, scale=FONT_SCALE_UI):
    w = text_width(text, scale)
    draw_text(surface, text, cx - w // 2, y, color, scale)


# ── game states ────────────────────────────────────────────────────────
STATE_MENU   = 0
STATE_PLAY   = 1
STATE_DEAD   = 2
STATE_PAUSE  = 3
STATE_HELP   = 4
STATE_ABOUT  = 5
STATE_SOUND  = 6

MENU_ITEMS = ("PLAY GAME", "HELP", "ABOUT", "SOUND SETTINGS", "EXIT GAME")
VOL_LABELS = ("LOW", "MID", "HIGH")
VOL_LEVELS = (0.12, 0.20, 0.32)

# ── nokia 3310 procedural sfx (files = off) ───────────────────────────
SAMPLE_RATE = 22050
NOKIA_DUTY  = 0.5


def _nokia_seq(notes, vol=0.20):
    """Build a square-wave tone sequence — no wav files."""
    buf = array.array("h")
    phase = 0.0
    amp = int(32767 * vol)
    for freq, dur in notes:
        n = max(1, int(SAMPLE_RATE * dur))
        step = freq / SAMPLE_RATE if freq > 0 else 0.0
        fade = max(1, n // 6)
        for i in range(n):
            if freq > 0:
                phase = (phase + step) % 1.0
                sample = amp if phase < NOKIA_DUTY else -amp
                if i >= n - fade:
                    sample = int(sample * (n - i) / fade)
            else:
                sample = 0
            buf.append(sample)
            buf.append(sample)
    try:
        return pygame.mixer.Sound(buffer=buf)
    except pygame.error:
        return None


class NokiaSFX:
    """3310-style beeps — all procedural, files = off."""

    def __init__(self):
        self.ok = False
        self.enabled = True
        self.vol_idx = 1  # MID
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512)
            self.sounds = {
                "eat":    _nokia_seq([(523, 0.04), (784, 0.06)]),
                "die":    _nokia_seq([(440, 0.10), (330, 0.10), (220, 0.12), (110, 0.22)]),
                "start":  _nokia_seq([(659, 0.05), (880, 0.07)]),
                "select": _nokia_seq([(880, 0.05)]),
                "pause":  _nokia_seq([(660, 0.04), (440, 0.04)]),
                "record": _nokia_seq([(523, 0.05), (659, 0.05), (784, 0.08)]),
            }
            self.ok = any(self.sounds.values())
        except pygame.error:
            self.sounds = {}

    @property
    def volume(self):
        return VOL_LEVELS[self.vol_idx]

    def toggle_enabled(self):
        self.enabled = not self.enabled

    def cycle_volume(self, direction=1):
        self.vol_idx = (self.vol_idx + direction) % len(VOL_LEVELS)

    def play(self, name):
        if not self.ok or not self.enabled:
            return
        snd = self.sounds.get(name)
        if snd:
            snd.set_volume(self.volume)
            snd.play()


class SnakeAssets:
    """Lorenzo Brooks / itspyguru Python-Games sprites — base64 in RAM, files = off."""

    def __init__(self):
        self.sprites = {}
        for name, chunks in ASSET_B64.items():
            data = base64.b64decode("".join(chunks))
            surf = pygame.image.load(io.BytesIO(data)).convert_alpha()
            self.sprites[name] = self._to_cell(surf)

        self.heads = {
            (0, -1): self.sprites["head_up"],
            (0, 1): self.sprites["head_down"],
            (-1, 0): self.sprites["head_left"],
            (1, 0): self.sprites["head_right"],
        }
        self.foods = [self.sprites[f"food_{i}"] for i in (1, 2, 3)]

    @staticmethod
    def _to_cell(surf):
        if surf.get_size() == (CELL, CELL):
            return surf
        return pygame.transform.smoothscale(surf, (CELL, CELL))

    @staticmethod
    def _rot(surf, direction):
        dx, dy = direction
        if (dx, dy) == (1, 0):
            return surf
        if (dx, dy) == (-1, 0):
            return pygame.transform.flip(surf, True, False)
        if (dx, dy) == (0, -1):
            return pygame.transform.rotate(surf, 90)
        if (dx, dy) == (0, 1):
            return pygame.transform.rotate(surf, -90)
        return surf

    def _body(self, prev, cur, nxt, index):
        d1 = (prev[0] - cur[0], prev[1] - cur[1])
        d2 = (nxt[0] - cur[0], nxt[1] - cur[1])
        anim = index % 2

        if d1[0] == -d2[0] and d1[1] == -d2[1]:
            if d1[0] != 0:
                return self.sprites[f"body_h{anim}"]
            return self.sprites[f"body_v{anim}"]

        cross = d1[0] * d2[1] - d1[1] * d2[0]
        corner = self.sprites["body_corner_l" if cross > 0 else "body_corner_r"]
        return self._rot(corner, d1)

    def piece(self, snake, index, direction):
        cur = snake[index]
        if index == 0:
            return self.heads.get(direction, self.heads[(1, 0)])

        prev = snake[index - 1]
        if index == len(snake) - 1:
            tail_dir = (cur[0] - prev[0], cur[1] - prev[1])
            return self._rot(self.sprites["tail"], tail_dir)

        return self._body(prev, cur, snake[index + 1], index)

    def food_sprite(self, kind):
        return self.foods[(kind - 1) % len(self.foods)]


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("[c] 1999-2026 acholding by ac snake my take 0.1")
        self.clock = pygame.time.Clock()
        self.lcd_surface = pygame.Surface((GRID_W, GRID_H))
        self.sfx = NokiaSFX()
        self.assets = SnakeAssets()
        self.state = STATE_MENU
        self.menu_sel = 0
        self.sound_row = 0
        self.high_score = 0
        self.quit_requested = False
        self.reset()

    def reset(self):
        mid_x = COLS // 2
        mid_y = ROWS // 2
        self.snake = [(mid_x, mid_y), (mid_x - 1, mid_y), (mid_x - 2, mid_y)]
        self.dir = (1, 0)
        self.next_dir = (1, 0)
        self.food = self._spawn_food()
        self.score = 0
        self.eat_flash = 0
        self.dead_timer = 0
        self.move_timer = 0
        self.move_interval = 0.10  # seconds between moves (nokia speed feel)
        self.blink_timer = 0
        self.food_anim = 0

    def _spawn_food(self):
        occupied = set(self.snake)
        free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in occupied]
        if not free:
            return None
        self.food_kind = random.randint(1, 3)
        return random.choice(free)

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.state == STATE_MENU:
            self._menu_input(event)

        elif self.state == STATE_HELP:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                self.state = STATE_MENU
                self.sfx.play("select")

        elif self.state == STATE_ABOUT:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                self.state = STATE_MENU
                self.sfx.play("select")

        elif self.state == STATE_SOUND:
            self._sound_input(event)

        elif self.state == STATE_PLAY:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if self.dir != (0, 1):
                    self.next_dir = (0, -1)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if self.dir != (0, -1):
                    self.next_dir = (0, 1)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if self.dir != (1, 0):
                    self.next_dir = (-1, 0)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if self.dir != (-1, 0):
                    self.next_dir = (1, 0)
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                self.state = STATE_PAUSE
                self.sfx.play("pause")

        elif self.state == STATE_PAUSE:
            if event.key in (pygame.K_ESCAPE, pygame.K_p, pygame.K_RETURN, pygame.K_SPACE):
                self.state = STATE_PLAY
                self.sfx.play("select")

        elif self.state == STATE_DEAD:
            if self.dead_timer > 0.5:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.reset()
                    self.state = STATE_PLAY
                    self.sfx.play("start")
                elif event.key == pygame.K_ESCAPE:
                    self.state = STATE_MENU
                    self.menu_sel = 0
                    self.sfx.play("select")

    def _menu_input(self, event):
        if event.key in (pygame.K_UP, pygame.K_w):
            self.menu_sel = (self.menu_sel - 1) % len(MENU_ITEMS)
            self.sfx.play("select")
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.menu_sel = (self.menu_sel + 1) % len(MENU_ITEMS)
            self.sfx.play("select")
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            choice = MENU_ITEMS[self.menu_sel]
            if choice == "PLAY GAME":
                self.reset()
                self.state = STATE_PLAY
                self.sfx.play("start")
            elif choice == "HELP":
                self.state = STATE_HELP
                self.sfx.play("select")
            elif choice == "ABOUT":
                self.state = STATE_ABOUT
                self.sfx.play("select")
            elif choice == "SOUND SETTINGS":
                self.state = STATE_SOUND
                self.sound_row = 0
                self.sfx.play("select")
            elif choice == "EXIT GAME":
                self.quit_requested = True
                self.sfx.play("select")

    def _sound_input(self, event):
        if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
            self.state = STATE_MENU
            self.sfx.play("select")
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.sound_row = (self.sound_row - 1) % 2
            self.sfx.play("select")
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.sound_row = (self.sound_row + 1) % 2
            self.sfx.play("select")
        elif event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
            direction = -1 if event.key in (pygame.K_LEFT, pygame.K_a) else 1
            if self.sound_row == 0:
                self.sfx.toggle_enabled()
                if self.sfx.enabled:
                    self.sfx.play("select")
            else:
                self.sfx.cycle_volume(direction)
                self.sfx.play("select")

    def update(self, dt):
        self.blink_timer += dt
        self.food_anim += dt

        if self.state == STATE_PLAY:
            self.move_timer += dt
            if self.eat_flash > 0:
                self.eat_flash -= dt

            if self.move_timer >= self.move_interval:
                self.move_timer -= self.move_interval
                self._step()

        elif self.state == STATE_DEAD:
            self.dead_timer += dt

    def _step(self):
        self.dir = self.next_dir
        hx, hy = self.snake[0]
        nx, ny = hx + self.dir[0], hy + self.dir[1]

        # wall collision
        if nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS:
            self._die()
            return

        # self collision
        if (nx, ny) in self.snake[:-1]:
            self._die()
            return

        self.snake.insert(0, (nx, ny))

        if self.food and (nx, ny) == self.food:
            self.score += 10
            self.eat_flash = 0.15
            self.sfx.play("eat")
            # speed up slightly — nokia feel
            self.move_interval = max(0.05, self.move_interval - 0.002)
            self.food = self._spawn_food()
            if self.food is None:
                # won the game
                self._die()
        else:
            self.snake.pop()

    def _die(self):
        self.state = STATE_DEAD
        self.dead_timer = 0
        new_record = self.score > self.high_score
        if new_record:
            self.high_score = self.score
        self.sfx.play("record" if new_record and self.score > 0 else "die")

    # ── rendering ─────────────────────────────────────────────────────
    def draw(self):
        self.screen.fill(BEZEL)

        # phone bezel
        bezel_rect = pygame.Rect(
            BEZEL_THICK, BEZEL_THICK,
            WIN_W - BEZEL_THICK * 2, WIN_H - BEZEL_THICK * 2
        )
        pygame.draw.rect(self.screen, BEZEL_LIGHT, bezel_rect, border_radius=8)
        inner = bezel_rect.inflate(-6, -6)
        pygame.draw.rect(self.screen, LCD_BORDER, inner, border_radius=5)

        # lcd area
        lcd_rect = pygame.Rect(
            BEZEL_THICK + PADDING,
            BEZEL_THICK + PADDING,
            GRID_W,
            GRID_H
        )
        self.lcd_surface.fill(LCD_BG)

        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state == STATE_HELP:
            self._draw_help()
        elif self.state == STATE_ABOUT:
            self._draw_about()
        elif self.state == STATE_SOUND:
            self._draw_sound_settings()
        elif self.state == STATE_PLAY:
            self._draw_game()
        elif self.state == STATE_DEAD:
            self._draw_game()
            self._draw_dead_overlay()
        elif self.state == STATE_PAUSE:
            self._draw_game()
            self._draw_pause_overlay()

        self.screen.blit(self.lcd_surface, lcd_rect.topleft)

        # score bar below lcd (in-game only)
        if self.state in (STATE_PLAY, STATE_PAUSE, STATE_DEAD):
            bar_y = lcd_rect.bottom + 8
            bar_x = lcd_rect.x
            self._draw_score_bar(bar_x, bar_y)

        pygame.display.flip()

    def _draw_grid(self):
        """Subtle nokia lcd grid lines."""
        for x in range(0, GRID_W, CELL):
            pygame.draw.line(self.lcd_surface, LCD_PIXEL, (x, 0), (x, GRID_H - 1))
        for y in range(0, GRID_H, CELL):
            pygame.draw.line(self.lcd_surface, LCD_PIXEL, (0, y), (GRID_W - 1, y))

    def _draw_game(self):
        self._draw_grid()

        # flash effect on eat
        if self.eat_flash > 0:
            flash_surf = pygame.Surface((GRID_W, GRID_H), pygame.SRCALPHA)
            alpha = int(60 * (self.eat_flash / 0.15))
            flash_surf.fill((*LCD_ON, alpha))
            self.lcd_surface.blit(flash_surf, (0, 0))

        # draw food — Lorenzo Brooks fruit sprites (GitHub/YouTube)
        if self.food:
            fx, fy = self.food
            pulse = 1.0 + 0.12 * ((self.food_anim * 4) % 1.0)
            size = max(8, int(CELL * pulse))
            food_surf = self.assets.food_sprite(self.food_kind)
            food_surf = pygame.transform.smoothscale(food_surf, (size, size))
            px = fx * CELL + (CELL - size) // 2
            py = fy * CELL + (CELL - size) // 2
            self.lcd_surface.blit(food_surf, (px, py))

        # draw snake — itspyguru/Python-Games Lorenzo Brooks sprites
        for i, (sx, sy) in enumerate(self.snake):
            sprite = self.assets.piece(self.snake, i, self.dir)
            self.lcd_surface.blit(sprite, (sx * CELL, sy * CELL))

        # border around play area
        pygame.draw.rect(self.lcd_surface, LCD_ON, (0, 0, GRID_W, GRID_H), 2)

    def _draw_menu(self):
        self._draw_grid()
        pygame.draw.rect(self.lcd_surface, LCD_ON, (0, 0, GRID_W, GRID_H), 2)

        ui_h = 7 * FONT_SCALE_UI
        draw_text_centered(self.lcd_surface, "SNAKE", GRID_W // 2, 10, LCD_TEXT)

        line_h = ui_h + 8
        start_y = 40
        for i, label in enumerate(MENU_ITEMS):
            y = start_y + i * line_h
            color = LCD_TEXT if i == self.menu_sel else LCD_TEXT_DIM
            prefix = "> " if i == self.menu_sel else "  "
            draw_text_centered(self.lcd_surface, prefix + label, GRID_W // 2, y, color)

        if self.high_score > 0:
            draw_text_centered(self.lcd_surface, f"HI:{self.high_score:04d}", GRID_W // 2, 178, LCD_TEXT_DIM)

        draw_text_centered(self.lcd_surface, "UP/DOWN  ENTER", GRID_W // 2, 248, LCD_TEXT_DIM)
        draw_text_centered(self.lcd_surface, "v0.1  files=off", GRID_W // 2, 274, LCD_PIXEL)

    def _draw_help(self):
        self._draw_grid()
        pygame.draw.rect(self.lcd_surface, LCD_ON, (0, 0, GRID_W, GRID_H), 2)

        ui_h = 7 * FONT_SCALE_UI
        draw_text_centered(self.lcd_surface, "HELP", GRID_W // 2, 12, LCD_TEXT)

        lines = [
            "ARROWS/WASD MOVE",
            "P OR ESC PAUSE",
            "EAT FOOD FOR +10",
            "AVOID WALLS AND",
            "YOUR OWN TAIL",
            "SPEED UP AS YOU",
            "GROW LONGER",
        ]
        y = 46
        for line in lines:
            draw_text_centered(self.lcd_surface, line, GRID_W // 2, y, LCD_TEXT_DIM)
            y += ui_h + 5

        if int(self.blink_timer * 2) % 2 == 0:
            draw_text_centered(self.lcd_surface, "ESC BACK", GRID_W // 2, 276, LCD_TEXT)

    def _draw_about(self):
        self._draw_grid()
        pygame.draw.rect(self.lcd_surface, LCD_ON, (0, 0, GRID_W, GRID_H), 2)

        ui_h = 7 * FONT_SCALE_UI
        draw_text_centered(self.lcd_surface, "ABOUT", GRID_W // 2, 12, LCD_TEXT)

        lines = [
            "AC'S SNAKE v0.1",
            "NOKIA 3310 STYLE",
            "LORENZO BROOKS ART",
            "GITHUB/YOUTUBE SNAKE",
            "BASE64 RAM EMBED",
            "FILES = OFF",
            "NO DISK READS",
        ]
        y = 48
        for line in lines:
            draw_text_centered(self.lcd_surface, line, GRID_W // 2, y, LCD_TEXT_DIM)
            y += ui_h + 6

        if int(self.blink_timer * 2) % 2 == 0:
            draw_text_centered(self.lcd_surface, "ESC BACK", GRID_W // 2, 276, LCD_TEXT)

    def _draw_sound_settings(self):
        self._draw_grid()
        pygame.draw.rect(self.lcd_surface, LCD_ON, (0, 0, GRID_W, GRID_H), 2)

        ui_h = 7 * FONT_SCALE_UI
        draw_text_centered(self.lcd_surface, "SOUND", GRID_W // 2, 12, LCD_TEXT)

        sound_on = "ON" if self.sfx.enabled else "OFF"
        vol_label = VOL_LABELS[self.sfx.vol_idx]
        rows = [
            ("SOUND", sound_on),
            ("VOLUME", vol_label),
        ]
        y = 78
        for i, (label, value) in enumerate(rows):
            sel = i == self.sound_row
            color = LCD_TEXT if sel else LCD_TEXT_DIM
            prefix = "> " if sel else "  "
            text = f"{prefix}{label}: {value}"
            draw_text_centered(self.lcd_surface, text, GRID_W // 2, y, color)
            y += ui_h + 18

        draw_text_centered(self.lcd_surface, "L/R CHANGE", GRID_W // 2, 200, LCD_TEXT_DIM)
        if int(self.blink_timer * 2) % 2 == 0:
            draw_text_centered(self.lcd_surface, "ESC BACK", GRID_W // 2, 276, LCD_TEXT)

    def _draw_dead_overlay(self):
        overlay = pygame.Surface((GRID_W, GRID_H), pygame.SRCALPHA)
        overlay.fill((*LCD_BG, 180))
        self.lcd_surface.blit(overlay, (0, 0))

        draw_text_centered(self.lcd_surface, "GAME OVER", GRID_W // 2, 82, LCD_TEXT)

        draw_text_centered(self.lcd_surface, f"SCORE:{self.score:04d}", GRID_W // 2, 132, LCD_TEXT)

        if self.score >= self.high_score and self.score > 0:
            if int(self.blink_timer * 3) % 2 == 0:
                draw_text_centered(self.lcd_surface, "NEW RECORD!", GRID_W // 2, 168, LCD_TEXT)

        if self.dead_timer > 0.5:
            if int(self.blink_timer * 2) % 2 == 0:
                draw_text_centered(self.lcd_surface, "PRESS ENTER", GRID_W // 2, 214, LCD_TEXT)

    def _draw_pause_overlay(self):
        overlay = pygame.Surface((GRID_W, GRID_H), pygame.SRCALPHA)
        overlay.fill((*LCD_BG, 160))
        self.lcd_surface.blit(overlay, (0, 0))

        ui_h = 7 * FONT_SCALE_UI
        draw_text_centered(self.lcd_surface, "PAUSED", GRID_W // 2, GRID_H // 2 - ui_h, LCD_TEXT)
        if int(self.blink_timer * 2) % 2 == 0:
            draw_text_centered(self.lcd_surface, "PRESS ESC", GRID_W // 2, GRID_H // 2 + 10, LCD_TEXT)

    def _draw_score_bar(self, x, y):
        """Draw score below the LCD in the bezel area."""
        label_color = LCD_TEXT
        dim_color = LCD_TEXT_DIM
        hud = FONT_SCALE_HUD

        draw_text(self.screen, f"SCR:{self.score:04d}", x + 4, y, label_color, hud)

        hi_text = f"HI:{self.high_score:04d}"
        w = text_width(hi_text, hud)
        draw_text(self.screen, hi_text, x + GRID_W - w - 4, y, dim_color, hud)

        len_text = f"<{len(self.snake)}>"
        lw = text_width(len_text, hud)
        draw_text(self.screen, len_text, x + (GRID_W - lw) // 2, y, dim_color, hud)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0  # 60 FPS, delta in seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_input(event)
                if self.quit_requested:
                    running = False

            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()


# ── entry point ───────────────────────────────────────────────────────
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
