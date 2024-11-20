package morkato.api.dto.validation;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import jakarta.validation.constraints.Pattern;

import java.lang.annotation.*;

@Pattern(regexp = "^(https?://)(?:www\\.)?[a-zA-Z0-9\\-\\.]{1,255}(?:/[a-zA-Z0-9\\-\\._~:\\/?#\\[\\]@!$&''()*+,;=]{0,255})?$")
@Target({ ElementType.FIELD, ElementType.METHOD, ElementType.PARAMETER, ElementType.ANNOTATION_TYPE })
@Retention(RetentionPolicy.RUNTIME) 
@Documented
@Constraint(validatedBy = {})
public @interface BannerSchema {
  String message() default "This banner is invalid!";
  Class<?>[] groups() default {};
  Class<? extends Payload>[] payload() default {};
}
