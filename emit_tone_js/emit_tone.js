let red: number[] = []
let green: number[] = []
let blue: number[] = []
let freq = 0
input.buttonA.onEvent(ButtonEvent.Click, function () {
    red = [255, 255, 204, 51, 0, 0, 0, 51, 204, 255]
    green = [0, 153, 255, 255, 255, 255, 102, 0, 0, 0]
    blue = [0, 0, 0, 0, 102, 255, 255, 255, 255, 153]
    music.setVolume(20)
    for (let index = 0; index <= 256; index++) {
        light.setAll(0x000000)
        freq = Math.round(1760 * (120 / 119) ** index)
        light.setPixelColor(index % 10, light.rgb(red[index % 10], green[index % 10], blue[index % 10]))
        console.log(freq)
        music.playTone(freq, 40)
        music.rest(40)
        if (input.buttonB.isPressed()) {
            light.clear()
            control.reset()
        }
    }
})
