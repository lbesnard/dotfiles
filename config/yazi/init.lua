-- Show sizes computed by what-size (only for items you calculated) on the right
function Linemode:whatsize()
  local cache = WHAT_SIZE_CACHE or {}
  return cache[tostring(self._file.url)] or ""
end
