SELECT 
    p.product_id AS old_product_id,
    pk.package_id AS old_package_id,
    dp.dict_product_id AS old_dict_product_id,
    p.code,
    p.description,
    p.short AS short_desc,
    pk.supplier_id,
    pk.reference AS supplier_code,
    pk.labels AS units_per_pack,
    pk.conservation_id,
    pk.in_the_dark,
    pk.picture,
    pk.note,
    pk.piece AS is_piece,
    dp.section_id,
    dp.category_id,
    dp.understock,
    dp.reorder AS reorder_qty,
    p.status
FROM products p
LEFT JOIN packages pk ON pk.product_id = p.product_id
LEFT JOIN dict_products dp ON dp.package_id = pk.package_id
ORDER BY p.product_id;