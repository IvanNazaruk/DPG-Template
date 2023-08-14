# Source: https://github.com/gre/bezier-easing/blob/master/src/index.js

from array import array
from typing import Callable

NEWTON_ITERATIONS = 4
NEWTON_MIN_SLOPE = 0.001
SUBDIVISION_PRECISION = 0.0000001
SUBDIVISION_MAX_ITERATIONS = 10

kSplineTableSize = 11
kSampleStepSize = 1.0 / (kSplineTableSize - 1.0)


def A(a1, a2):
    return 1.0 - 3.0 * a2 + 3.0 * a1


def B(a1, a2):
    return 3.0 * a2 - 6.0 * a1


def C(a1):
    return 3.0 * a1


def calcBezier(t, a1, a2):
    return ((A(a1, a2) * t + B(a1, a2)) * t + C(a1)) * t


def getSlope(t, a1, a2):
    return 3.0 * A(a1, a2) * t * t + 2.0 * B(a1, a2) * t + C(a1)


def binarySubdivide(x, a, b, x1, x2):
    i = 0
    while True:
        currentT = a + (b - a) / 2.0
        currentX = calcBezier(currentT, x1, x2) - x
        if currentX > 0.0:
            b = currentT
        else:
            a = currentT
        if abs(currentX) <= SUBDIVISION_PRECISION or i >= SUBDIVISION_MAX_ITERATIONS:
            break
        i += 1
    return currentT


def newtonRaphsonIterate(x, guess_t, x1, x2):
    for i in range(NEWTON_ITERATIONS):
        currentSlope = getSlope(guess_t, x1, x2)
        if currentSlope == 0.0:
            return guess_t
        currentX = calcBezier(guess_t, x1, x2) - x
        guess_t -= currentX / currentSlope
    return guess_t


def LinearEasing(x: float) -> float:
    return x


def bezier(x1: float, y1: float, x2: float, y2: float) -> Callable[[float], float]:
    if not (0 <= x1 <= 1 and 0 <= x2 <= 1):
        raise ValueError("bezier x values must be in [0, 1] range")

    if x1 == y1 and x2 == y2:
        return LinearEasing

    sampleValues = array("f", [0] * kSplineTableSize)
    for i in range(kSplineTableSize):
        sampleValues[i] = calcBezier(i * kSampleStepSize, x1, x2)

    def getTForX(x: float) -> float:
        intervalStart = 0.0
        currentSample = 1
        lastSample = kSplineTableSize - 1

        while currentSample != lastSample and sampleValues[currentSample] <= x:
            currentSample += 1
            intervalStart += kSampleStepSize
        currentSample -= 1

        # Interpolate to provide an initial guess for t
        dist = (x - sampleValues[currentSample]) / (sampleValues[currentSample + 1] - sampleValues[currentSample])
        guessForT = intervalStart + dist * kSampleStepSize

        initialSlope = getSlope(guessForT, x1, x2)
        if initialSlope >= NEWTON_MIN_SLOPE:
            return newtonRaphsonIterate(x, guessForT, x1, x2)
        elif initialSlope == 0.0:
            return guessForT
        else:
            return binarySubdivide(x, intervalStart, intervalStart + kSampleStepSize, x1, x2)

    def BezierEasing(x: float) -> float:
        if x == 0 or x == 1:
            return x
        return calcBezier(getTForX(x), y1, y2)

    return BezierEasing
