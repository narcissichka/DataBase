-- Table: public.Catalog

-- DROP TABLE public."Catalog";

CREATE TABLE IF NOT EXISTS public."Catalog"
(
    id_catalog integer NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    id_shop integer NOT NULL,
    pid_catalog integer NOT NULL,
    CONSTRAINT "Catalog_pkey" PRIMARY KEY (id_catalog),
    CONSTRAINT "Catalog_id_shop_fkey" FOREIGN KEY (id_shop)
        REFERENCES public."Shop" (id_shop) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT pid_catalog_fkey FOREIGN KEY (pid_catalog)
        REFERENCES public."Catalog" (id_catalog) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE public."Catalog"
    OWNER to postgres;