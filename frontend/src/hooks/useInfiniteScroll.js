// src/hooks/useInfiniteScroll.js
import { useRef, useCallback } from "react";

export function useInfiniteScroll(callback, options = {}) {
  const observer = useRef();

  const lastElementRef = useCallback(
    (node) => {
      if (observer.current) observer.current.disconnect();
      observer.current = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
          callback();
        }
      }, options);
      if (node) observer.current.observe(node);
    },
    [callback, options]
  );

  return lastElementRef;
}
