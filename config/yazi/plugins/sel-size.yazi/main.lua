--- @since 25.5.31
-- Calculate the size of the selected items (or the hovered one) and store it
-- in the global WHAT_SIZE_CACHE, displayed by Linemode:whatsize() in init.lua

local get_targets = ya.sync(function()
  local urls = {}
  for _, u in pairs(cx.active.selected) do
    urls[#urls + 1] = tostring(u.url or u)
  end
  if #urls == 0 then
    local h = cx.active.current.hovered
    if h then
      urls[1] = tostring(h.url)
    end
  end
  return urls
end)

local store = ya.sync(function(_, sizes)
  WHAT_SIZE_CACHE = WHAT_SIZE_CACHE or {}
  for k, v in pairs(sizes) do
    WHAT_SIZE_CACHE[k] = v
  end
  ui.render()
end)

local function format_size(size)
  local units = { "B", "KB", "MB", "GB", "TB" }
  local i = 1
  while size >= 1024 and i < #units do
    size = size / 1024
    i = i + 1
  end
  return i == 1 and string.format("%d B", size) or string.format("%.1f %s", size, units[i])
end

return {
  entry = function()
    local sizes = {}
    for _, path in ipairs(get_targets()) do
      local it = fs.calc_size(Url(path))
      if it then
        local total = 0
        while true do
          local n = it:recv()
          if not n then
            break
          end
          total = total + n
        end
        sizes[path] = format_size(total)
      end
    end
    store(sizes)
  end,
}
