class ImmediateIntersectionObserver {
  constructor(callback) {
    this.callback = callback;
  }
  observe(element) {
    // Immediately trigger the callback, simulating that the element is intersecting.
    this.callback([{ target: element, isIntersecting: true }]);
  }
  unobserve() {}
  disconnect() {}
}
window.IntersectionObserver = ImmediateIntersectionObserver;
