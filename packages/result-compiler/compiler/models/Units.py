from typing import Annotated

from pydantic import Field

type NonZeroInt = Annotated[int, Field(gt=0)]
type NonZeroFloat = Annotated[float, Field(gt=0)]
