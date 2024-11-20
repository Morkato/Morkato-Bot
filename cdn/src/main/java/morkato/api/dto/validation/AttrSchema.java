package morkato.api.dto.validation;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import jakarta.validation.constraints.Digits;

import java.lang.annotation.*;

@Target({ ElementType.FIELD, ElementType.METHOD, ElementType.PARAMETER, ElementType.ANNOTATION_TYPE })
@Digits(integer = 12, fraction = 0)
@Retention(RetentionPolicy.RUNTIME) 
@Documented
@Constraint(validatedBy = {})
public @interface AttrSchema {
  String message() default "This attribute is invalid!";
  Class<?>[] groups() default {};
  Class<? extends Payload>[] payload() default {};
}
