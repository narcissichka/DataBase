-- Table: public.Order

-- DROP TABLE public."Order";

CREATE TABLE IF NOT EXISTS public."Order"
(
    id_order integer NOT NULL,
    customer_name character varying COLLATE pg_catalog."default" NOT NULL,
    id_shop integer NOT NULL,
    date timestamp without time zone NOT NULL,
    CONSTRAINT "Order_pkey" PRIMARY KEY (id_order),
    CONSTRAINT "Order_id_shop_fkey" FOREIGN KEY (id_shop)
        REFERENCES public."Shop" (id_shop) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE public."Order"
    OWNER to postgres;