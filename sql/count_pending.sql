SELECT COUNT(*) FROM items i
JOIN requests r ON r.request_id = i.request_id
WHERE r.status = 0 AND i.status = 1;