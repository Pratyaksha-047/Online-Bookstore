gsap.registerPlugin(ScrollTrigger);

let tl2 = gsap.timeline();
tl2.to("#scrollingText", {
  x: 1000,
  duration: 50,
  repeat: -1,
  ease: 'linear'
})
let tl = gsap.timeline();
tl.to('#scrollingText', {
  xPercent: 15,
  scrollTrigger: {
    trigger: "#scrollingText",
    scrub: 1
  }
})