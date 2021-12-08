gsap.registerPlugin(ScrollTrigger);

gsap.to(".hero-title", {
  x: -1300,
  backgroundPosition: '1300px 0',
  scrollTrigger: {
    trigger: "body",
    start: 'top top',
    scrub: true,
  }
});

gsap.to(".hero-cta", {
  y: 80,
  scrollTrigger: {
    trigger: "body",
    start: 'top top',
    end: 'bottom top',
    scrub: true,
  }
});