-- Table: public.Product

-- DROP TABLE public."Product";

CREATE TABLE IF NOT EXISTS public."Product"
(
    id_product integer NOT NULL,
    title character varying COLLATE pg_catalog."default" NOT NULL,
    price integer NOT NULL,
    category character varying COLLATE pg_catalog."default" NOT NULL,
    id_catalog integer NOT NULL,
    id_order integer NOT NULL,
    CONSTRAINT "Product_pkey" PRIMARY KEY (id_product),
    CONSTRAINT "Product_id_catalog_fkey" FOREIGN KEY (id_catalog)
        REFERENCES public."Catalog" (id_catalog) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "Product_id_order_fkey" FOREIGN KEY (id_order)
        REFERENCES public."Order" (id_order) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE public."Product"
    OWNER to postgres;

COMMENT ON COLUMN public."Product".id_order
    IS '(UNIQUE)';